# CEA_Wrap
A Python-Based wrapper for the NASA CEA Thermochemical Code

# Installation Instructions
We are now on PyPi!

In a command prompt type ```pip install --upgrade CEA_Wrap``` to upgrade/install CEA_Wrap
Click on "releases" on the right side of the main page and download the .zip file.

You can now import it as any other python module with ```import CEA_Wrap```. Whenever you import the file, it will put the required thermo.lib and trans.lib files into your current directory.

# Examples
You can view the "very_simple_example.py" file in this repository for examples on use.

# Documentation
## Specifying Materials
  In order to run problems, you must create materials. Materials must be either Fuel or Oxidizer (F or O) objects
  
  ### Constructor Parameters:
  ```__init__(name, temp=298, wt_percent=None, mols=None, chemical_composition = None, hf = None):```
  
* name: required parameter, the CEA material name with correct spelling. E.G. aluminum is "Al(cr)" and methane is "CH4". 
  * If you specify chemical_composition, name can be whatever single word you want
* temp: default 298, specified reactant temperature, kelvin
* wt_percent: A weight-based percentage for the element. Weight percentages do not need to add up to 100, and are calculated on the ratio with other Fuels/Oxidizers
* mols: A mol-based percentage for the element. Can be used as in Oxidizer("O2", mols=1) and Oxidizer("N2", mols=3.76) for air (except CEA has "air" as a reactant...)
* **NOTE:** wt_percent and mols cannot be specified together, if neither is defined, the Material gets a wt_percent of 1
* chemical_composition: chemical composition such as "LI 1 B 1 H 4" for LiBH4. If defined, will not use CEA default values 
  * **NOTE: UNTESTED**
* hf:  Enthalpy of formation, kJ/kg, must be specified if chemical_composition is specified
  * **NOTE: UNTESTED**

## Generic Problem Methods:
  ### Constructor Parameters (making new Problem Objects):
  ```__init__(*, **kwargs)```:
* **NOTE:** all parameters must be specified by keyword, e.g. problem = RocketProblem(pressure=500, massf=True)
* pressure: default 1000, Initial problem pressure
  * pressure can be specified later with .set_pressure
* materials: default None, List of Material objects, order doesn't matter, of Oxidizer and Fuel objects e.g. materials=[material1, material2, ...]
  * materials can be specified later with .set_materials([material1, material2, ...])
  * materials can also be specified when you run a problem like problem.run_cea(material1, material2, ...)
  * materials MUST all have wt_percent specified or all have mols specified, can't have mixtures.
* massf: default False, CEA usually outputs product ratios in mole ratios, if massf is True, mass ratios are specified
  * massf can be specified later with .set_massf
* filename: default "my_output", the filename we save our .inp files to and CEA saves our .out and .plt to.
  * DO NOT INCLUDE ".inp" IN YOUR FILENAMES. Do not include any slashes.
  * filename can be specified later with .set_filename
* pressure_units: default "psi", the units that your input pressure is in. Possible values are "bar", "atm", "psi", or "mmh"
  * pressure_units can be specified later with .set_pressure_units
* inserts: default None, a list of CEA names for species which should be forced into the product considerations
  * Tip: If you are doing calculations with Aluminum, I recommend using inserts=["AL2O3(L)", "AL2O3(a)"]
* omits: default None, a list of CEA names for species which should be specifically ignored in the product considerations
* **NOTE:** You must specify one of the following reactant ratio schemes. Either during initialization with x=1.0 or later with problem.set_x(1.0) where x is p_f, o_f, etc.
#### Specifying reactant ratios:
   Key  | CEA Key | Description
  ------|---------|---------------------------------------------------------------------------------------------------------
   p_f  |  %f     | Percent fuel by weight
   f_o  |  f/o    | Fuel-to-oxidant weight ratio
   o_f  |  o/f    | Oxidant-to-fuel weight ratio
   phi  |  phi    | Equivalence ratios in terms of fuel-to-oxidant weight ratios (eq. (9.19) in Gordon and McBride, 1994)
   r_eq |  r      | Chemical equivalence ratios in terms of valences (eq. (9.18) in Gordon and McBride, 1994)

### Available Methods
#### ```data = run_cea(*materials)```
   
Run the CEA problem, returning an "Output" dictionary (keys and values specified later in this documentation)
* Inputs are an optional material list. If materials are not specified as an initial parameter or with .set_materials, you can list them here.
  
#### ```set_absolute_o_f()```
Have you ever specified all your components in absolute percentages, and then have to manually calculate the o_f ratio based on what is fuel and what is oxidizer?

Well no more! Just call this function and we calculate the correct o_f ratio for you so that your absolute percentages are correctly reflected in the problem.
  Functions off of the existing material list, so call this after setting materials

## Rocket Problem Constructor Additional Parameters:
* sup: default 1, supersonic exit/throat area ratio
  * sup can be specified later with .set_sup
* sub: default None, subsonic exit/throat area ratio
  * sub can be specified later with .set_sub
* **NOTE:** sup and sub cannot be specified at the same time
* ae_at: default None, exit/throat area ratio (alias for sup)
  * ae_at can be specified later with .set_ae_at
* analysis_type: default "equilibrium", whether to use equilibrium reactions or frozen. For using frozen specify "frozen" or "frozen nfz=1" for frozen at the chamber or "frozen nfz=2" for frozen at the throat

## Available Output Dictionary Keys:
All output objects are "Output" objects, which are similar to dictionaries, but can also be accessed with dot notation.

For example if you had "data = problem.run_cea()", and wanted pressure, you could do either data.p or data["p"]

In addition, all product dictionaries are also "Output"s so to get H2O composition, you could use data.prod_c.H2O or data["prod_c"]["H2O"] or data["prod_c"].H2O, etc.

### Detonation:
* prod_c - dictionary of chamber products, in mole or mass fractions (as specified in problem)
* p - pressure, bar
* t - temperature, Kelvin
* h - enthalpy, kJ/kg
* rho - density, kg/m^3
* son - sonic velocity, m/s
* visc - burned gas viscosity, Pascal-Seconds
* mw - molecular weight of products, kg/kmol
* cp - constant-pressure specific heat capacity, kJ/(kg*K)
* gammas - isentropic ratio of specific heats
* gamma - "real" ratio of specific heats (multiplied by -(dLV/dLP)t)
* vel - detonation velocity, m/s
* mach - detonation mach number
* p_p1 - P/P1, ratio of detonation pressure to initial pressure
* t_t1 - T/T1, ratio of detonation temperature to initial pressure
* m_m1 - M/M1, ratio of detonation molecular weight to initial molecular weight
* rho_rho1 - RHO/RHO1, ratio of detonation density to initial density
* dLV_dLP_t - (dLV/dLP)t, used to convert isentropic gamma to real gamma
* dLV_dLT_p - (dLV/dLT)p
* phi - weight-based equivalence ratio of oxidizer/fuel
### HP (Specified Enthalpy and Pressure):
* prod_c - dictionary of chamber products, in mole or mass fractions (as specified in problem)
* p - pressure, bar
* t - temperature, Kelvin
* h - enthalpy, kJ/kg
* rho - density, kg/m^3
* son - sonic velocity, m/s
* visc - burned gas viscosity, Pascal-Seconds
* mw - molecular weight of products, kg/kmol
* cp - constant-pressure specific heat capacity, kJ/(kg*K)
* gammas - isentropic ratio of specific heats
* gamma - "real" ratio of specific heats (multiplied by -(dLV/dLP)t)
* dLV_dLP_t - (dLV/dLP)t, used to convert isentropic gamma to real gamma
* dLV_dLT_p - (dLV/dLT)p
* phi - weight-based equivalence ratio of oxidizer/fuel
### Rocket:
* **NOTE : Properties are by default at exit. Chamber parameters are prefixed "c_" and throat properties "t_"**
* **NOTE : Properties not defined for frozen flow are marked with an asterisk (*)**
* prod_c - dictionary of chamber products, in mole or mass fractions (as specified in problem)
* \*prod_t - dictionary of throat products, in mole or mass fractions (as specified in problem)
* \*prod_e - dictionary of exit products, in mole or mass fractions (as specified in problem)
* p - pressure, bar
  * t_p - throat
  * c_p - chamber
* t - temperature, Kelvin
  * t_t - throat
  * c_t - chamber
* h - enthalpy, kJ/kg
  * t_h - throat
  * c_h - chamber
* rho - density, kg/m^3
  * t_rho - throat
  * c_rho - chamber
* son - sonic velocity, m/s
  * t_son - throat
  * c_son - chamber
* visc - burned gas viscosity, Pascal-Seconds
  * t_visc - throat
  * c_visc - chamber
* mw - molecular weight of all products, kg/kmol
  * t_mw - throat
  * c_mw - chamber
* m - molecular weight calculated as the weight of all products divided by the number of gaseous moles (0 if no condensed phases as mw=m), kg/kmol
  * t_m - throat
  * c_m - chamber
* cp - constant-pressure specific heat capacity, kJ/(kg*K)
  * t_cp - throat
  * c_cp - chamber
* gammas - isentropic ratio of specific heats
  * t_gammas - throat
  * c_gammas - chamber
* gamma - "real" ratio of specific heats (multiplied by -(dLV/dLP)t) (same as gammas for frozen flow)
  * t_gamma - throat
  * c_gamma - chamber
* isp - ideal isp (ambient pressure = exit pressure), s
  * t_isp - throat
* ivac - vacuum isp, s
  * t_ivac - throat
* cf - ideally expanded thrust coefficient
  * t_cf - throat
* \*dLV_dLP_t - (dLV/dLP)t, multiply gammas by negative this to convert isentropic gamma to real gamma
  * \*t_dLV_dLP_t - throat
  * \*c_dLV_dLP_t - chamber
* \*dLV_dLT_p - (dLV/dLT)p
  * \*t_dLV_dLT_p - throat
  * \*c_dLV_dLT_p - chamber
* cstar - characteristic velocity in chamber, m/s
* \*mach - mach number at exhaust
* o_f - oxidizer/fuel weight ratio
* phi - weight-based equivalence ratio of oxidizer/fuel
