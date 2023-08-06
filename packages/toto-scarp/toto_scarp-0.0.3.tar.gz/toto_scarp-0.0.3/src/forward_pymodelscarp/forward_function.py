# -*- coding: utf-8 -*-
"""

@author: Maureen Llinares, adapted for python from:
    
    Schlagenhauf A., Gaudemer Y., Benedetti L., Manighetti I., Palumbo L.,
    Schimmelpfennig I., Finkel R., Pou K.
    G.J.Int., 2010
    
    Tesson & Benedetti, G.J.Int., 2019
    
"""

import numpy as np
from numpy import pi, sin
import cl36_concentration as cl36


def mds(param, constants, seismic_scenario, scaling_factors, Ni):
    
    """ This function will calculate the synthectic 36Cl profile given a specific seismic scenario 
    and site parameters
    
    INPUTS : param, parameters of the site
             constants, global constants, dtype : dictionary
             seismic_scenario, dtype : dictionary
             scaling_factors, calculated with geometric_scaling.py, dtype: dictionary
             Ni, cl36 inherited concentration
    
    OUTPUTS : Nf, final 36Cl concentration (at/g), dtype : numpy array
    
    Modify your site parameters in the "site_parameters.py" file
    Modify your seismic scenario in the "seismic_scenario.py" file
    Return the synthetic profile
    
    Adapted for python from: 
    
    Schlagenhauf A., Gaudemer Y., Benedetti L., Manighetti I., Palumbo L.,
    Schimmelpfennig I., Finkel R., Pou K.
    G.J.Int., 2010
    
    Tesson & Benedetti, G.J.Int., 2019 """
    
    out_debug={}
    # site parameters (see site_parameters.py)
    alpha = param.alpha # colluvial wedge slope
    beta = param.beta # fault-plane slope
    
    Hfinal = param.Hfinal # total post-glacial height of the fault-plane, must include the depth of sample taken below the collucial wedge surface.
    rho_coll = param.rho_coll # colluvial wedge mean density
    rho_rock = param.rho_rock  # rock sample mean density
    thick = param.thick.copy()
    th2 = param.th2.copy()  # 1/2 thickness converted in g.cm-2
    h = param.h.copy()   # initial positions of the samples at surface (cm)- integer
    Z = param.Z.copy()

    
    # import data files (see site_parameters.py)
    data = param.data.copy()
    coll = param.coll.copy()
    EL = param.sf.copy()
    
    # input seismic scenario (see site_parameters.py)
    age = seismic_scenario['ages']
    slip = seismic_scenario['slips']
    epsilon = seismic_scenario['erosion_rate'] 
    preexp = seismic_scenario['preexp']

    # Constants
    lambda36 = constants['lambda36'] # Radioactive decay constant for 36Cl (a-1)
    
    # Scaling factors
    S_S = scaling_factors['S_S']
    Lambda_f_e = scaling_factors['Lambda_f_e']
    so_f_e = scaling_factors['so_f_e']
    Lambda_f_diseg = scaling_factors['Lambda_f_diseg']
    so_f_diseg = scaling_factors['so_f_diseg']
    Lambda_f_beta_inf = scaling_factors['Lambda_f_beta_inf']
    so_f_beta_inf = scaling_factors['so_f_beta_inf']
    
    """ VARIABLE INITIALIZATION """
        
    # Loading of Earth magnetic field variations from file 'EL'
    if preexp == 1: 
        EL[1,:]=EL[0,:]
        EL[1,0]=1
        EL[1,1]=1
    
    if age[0] == 1: 
        EL[1,]=EL[1,:]
        EL[1,0]=0
        EL[1,1]=1 
    
    # if preexp > np.sum(EL(:,2))
    #     error('The scaling factor file is not long enough to cover the full pre-exposure')
    
    ti = EL[:,0]  # time period (years)
    it = EL[:,1]  # time steps (years) - should be 100 yrs
    EL_f = EL[:,2]  # scaling factor for neutrons (S_el,f)
    EL_mu = EL[:,3]  # scaling factor for muons (S_el,mu)
    # Positions along e initially (eo)
    
    
    N_eq = len(age)  # number of earthquakes

    R = np.sum(slip)  # total cumulative slip
    Rc = np.cumsum(slip)   
    Rc = np.hstack((0, Rc)) # slip added up after each earthquake

    d = data.copy()  # substitution of matrix data by matrix d
    d[:,62] = Z.copy()  # samples position along z
    d[:,63] = (thick.copy())*rho_rock  # thickness converted in g.cm-2

    slip_gcm2 = slip * rho_coll  # coseismic slip in g.cm-2
    sc = np.cumsum(slip_gcm2)  # cumulative slip after each earthquake (g.cm-2)
    sc0 = np.hstack((0, sc)) 
    Nf = np.zeros(len(Z))  # Nf : final 36Cl concentration 

    eo = np.zeros(len(Z)) 

    for iseg in range (0, N_eq):
        eo[np.where((Z > sc0[iseg]) & (Z <= sc0[iseg + 1]))] = epsilon*age[iseg]*0.1*rho_rock  # in g.cm-2
    
   
    eo[0:len(Z)] = epsilon*age[0]*0.1*rho_rock 
    eo = eo + th2  # we add the 1/2 thickness : sample position along e is given at the sample center

    
    """ SEISMIC PHASE
    
    the term 'segment' is used for the samples exhumed by an earthquake-
    Calculation of [36Cl] profiles during seismic cycle.
    
    Separated in two stages : 
      1) When samples are at depth and progressively rising because of earthquakes
         (moving in the direction z with their position in direction e fixed)
      2) When samples are brought to surface and only sustaining erosion
         (moving along the direction e)
         
    FIRST EXHUMED SEGMENT is treated alone."""

    
    j1 = np.where((Z >= sc0[0]) & (Z <= sc0[1]))[0]  # Averf samples from first exhumed segment 
    N1 = np.zeros(len(Z[j1])) 
    tt = np.where(ti <= age[0])[0]  # epoch index more recent than first earthquake
    ip = it[tt]  # time intervals corresponding


    # C1 - Loop - iteration on samples (k) from first exhumed segment
    for k in range (0, len(j1)):
        
        djk = np.array(d[j1[k],:].copy())
        hjk = h[j1[k]]   # position of sample k (cm)
        N_in = float(Ni[j1[k]])  # initial concentration is Ni, obtained after pre-exposure
        
        ejk = eo[j1[k]]   # initial position along e is eo(j1(k)) 
        
        # C2 - Loop - iteration on  time steps ii from t1 (= age eq1) to present
        for ii in range (0, len(tt)):
            
            P_cosmo, P_rad = cl36.clrock(djk, ejk, Lambda_f_e, so_f_e, EL_f[tt[ii]], EL_mu[tt[ii]]) 
            scorr = S_S[1+int(hjk)]/S_S[0]      # surface scaling factor (scorr)
            P_tot = P_rad + P_cosmo*scorr            # only Pcosmogenic is scaled with scorr
            N_out = N_in + (P_tot - lambda36*N_in)*ip[ii]  # minus radioactive decrease during same time step
            
            ejk = ejk - epsilon*ip[ii]*0.1*rho_rock  # new position along e at each time step (g.cm-2)
            N_in = N_out  
        N1[k] = N_out # AVERF
        


    Nf[j1] = N1 

    # ITERATION ON SEGMENTS 2 to N_eq
    
    # C3 - Loop - iteration on each segment (from segment 2 to N_eq=number of eq)
    for iseg in range (1, N_eq):
            
        j = np.where((Z > sc0[iseg]) & (Z <= sc0[iseg+1]))[0]  # index of samples from segment iseg
        z_j = Z[j]  # initial depth along z of these samples (g.cm-2)
        N_new = np.zeros(len(z_j))
        
        # C4 - Loop - iteration each sample from segment iseg     
        for k in range (0, len(j)) :                                                  
            
            ejk = eo[j[k]]  # initial position along e is stil eo.
            djk = d[j[k],:]
            djk[62] = djk[62]*sin((beta - alpha)*pi/180) # AVERF 
            
            N_in = Ni[j[k]]  #  initial concentration is Ni
            
            # C5 - Loop - iteration on previous earthquakes
            for l in range (0, iseg):                                                     
                ttt = np.where((ti <= age[l]) & (ti > age[l+1]))[0]  # epoch index 
                ipp = it[ttt]  # time intervals corresponding
                
                # depth (along z) are modified after each earthquake
                
                djk[62] = djk[62] - (slip[l]*rho_coll*sin((beta - alpha) *pi/180)) # AVERF 
                d0 = djk.copy()
                d0[62] = 0 
                

                #------------------------------            
                # C6 - DEPTH LOOP - iteration during BURIED PERIOD (T1 -> T(iseg-1))
                #------------------------------ 
                for iii in range (0, len(ttt)):
                    P_cosmo,P_rad = cl36.clrock(djk, ejk, Lambda_f_e, so_f_e, EL_f[ttt[iii]], EL_mu[ttt[iii]]) 
                    # scaling at depth due to the presence of the colluvium: scoll=Pcoll(j)/Pcoll(z=0)
                    P_coll = cl36.clcoll(coll, djk, Lambda_f_diseg[l+1], so_f_diseg[l+1], EL_f[ttt[iii]], EL_mu[ttt[iii]]) 
                    P_zero = cl36.clcoll(coll, d0, Lambda_f_beta_inf, so_f_beta_inf, EL_f[ttt[iii]], EL_mu[ttt[iii]]) 
                    scoll = P_coll/P_zero  
                    
                    P_tot = P_rad + P_cosmo*scoll # only P (Pcosmogenic) is scalled by scoll
                    N_out = N_in + (P_tot - lambda36*N_in)*ipp[iii] # minus radioactive decrease during same time step
                    N_in = N_out
               
                
                N_in = N_out  
                

            N_in = N_out 
            
            tt = np.where(ti <= age[iseg])[0]  # epoch index more recent than earthquake iseg
            ip = it[tt] # time intervals corresponding
            djk = d[j[k],:]
            hjk = h[j[k]]
          
            #------------------------------         
            # C7 - SURFACE LOOP - iteration during EXHUMED PERIOD 
            
            for ii in range (0, len(tt)):
                P_cosmo,P_rad = cl36.clrock(djk,ejk,Lambda_f_e,so_f_e,EL_f[tt[ii]],EL_mu[tt[ii]]) 
                    
                scorr = S_S[1+int(hjk)]/S_S[0]  # surface scaling factor (scorr)
                P_tot = P_rad + P_cosmo*scorr  # only Pcosmogenic is scaled with scorr
                N_out = N_in + (P_tot - lambda36*N_in)*ip[ii]  # minus radioactive decrease during same time step
                  
                ejk = ejk - epsilon*ip[ii]*0.1*rho_rock  # new position along e at each time step (g.cm-2)
                N_in = N_out
                
            
            N_new[k] = N_out

       
        Nf[j] = N_new 
        
    return Nf, h, out_debug    

