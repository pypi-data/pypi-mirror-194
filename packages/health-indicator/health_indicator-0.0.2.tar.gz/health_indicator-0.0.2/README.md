# health-indicator

## Reference
Main Maintainer: Jesse E.Agbe(JCharis)
Jesus Saves @JCharisTech
https://www.youtube.com/watch?v=ueuLe4PipiI

### Features
+ Collection of Health Indices
	- BMI
	- BAI
	- Corpulence Index
	- Piglet Indices
	- etc 
+ Collection of Health Indicators
	- Mortality rate
	- Birth rate
	- Prevalence Rate
	- Fertility rate


### Getting Started
The package can be found on pypi hence you can install it using pip

#### Installation
```bash
pip install health-indicator
```

### Usage
Using the short forms or abbreviated forms of indices
```python
>>> from health_indicator import bmi
>>> bmi(54,1.70)

```

Using the long form of indices
```python
>>> from health_indicator import bodymassindex
>>> bodymassindex(54,1.70)

```