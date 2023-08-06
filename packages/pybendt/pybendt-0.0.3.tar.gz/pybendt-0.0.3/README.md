# pybendt
Brownian Elastic Networks with Dynamic Topology.

Copyright &copy;2023- Tomasz Skóra [tskora@sci.utah.edu](mailto:tskora@sci.utah.edu)

> **Warning**
> 
> The software is not extensively tested yet! It's just a prototype!

## Features

- [x] Brownian dynamics w/o hydrodynamic interactions
- [x] customizable atom-atom (2-body) interactions
- [ ] customizable many-body interactions
- [x] customizable event-driven bond topology changes

## Quick start

To install, type following commands in a terminal:
```shell
$ pip3 install pybendt
```

## Units

| Physical property | Units |
|---|---|
| Temperature | kelvin (*K*) |
| Friction coefficient | picosecond times kilocalorie per mole per angstrom squared (*ps kcal/mol/Å^2*) |
| Time | picosecond (*ps*) |
| Distance | angstrom (*Å*) |
| Energy | kilocalorie per mole (*kcal/mol*) |
| Force | kilocalorie per mole per angstrom (*kcal/mol/Å*) |
| Force constant | kilocalorie per mole per angstrom squared (*kcal/mol/Å^2*) |

> **Note**
> 
> There is a separate function ``friction_from_hydrodynamic_radius_and_viscosity`` which takes hydrodynamic radius in angstrom (*Å*) and viscosity in centipoise (*cP*) and returns friction coeffiient in picosecond times kilocalorie per mole per angstrom squared (*ps kcal/mol/Å^2*).

## Authors

The following people contributed to the development of pybendt.

- Tomasz Skóra -- **creator, lead developer** (contact: tskora@sci.utah.edu)
