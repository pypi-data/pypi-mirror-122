# Pyffect

Get inspiration from https://github.com/MaT1g3R/option and Scala type system

Try to support `mypy` type annotation.

You can use following types from this library
- Option
- Some
- NONE
- Either
- Left 
- Right
- Unit

### Option Type Usage
```python
from pyffect import Option, NONE, Some


def findDistanceFromSun(planetName: str) -> Option[str]:
    planetAndDistance = {
        "Mercury": "0.39 AU",
        "Venus": "0.72 AU",
        "Earth": "1.00 AU",
        "Mars": "1.52 AU",
        "Jupiter": "5.20 AU",
        "Saturn": "9.54 AU",
        "Uranus": "19.20 AU",
        "Neptune": "30.06 AU",
    }

    if planetName in planetAndDistance:
        return Some(planetAndDistance[planetName])
    else:
        return NONE()


distanceFromJupiterOrNone: Option[str] = findDistanceFromSun("Jupiter")
assert distanceFromJupiterOrNone.isDefined
assert distanceFromJupiterOrNone.value == "5.20 AU"

distanceFromUnknownPlanetOrNone: Option[str] = findDistanceFromSun("Unknown Planet")
assert distanceFromUnknownPlanetOrNone.isEmpty
assert distanceFromUnknownPlanetOrNone.getOrElse("Unknown Distance") == "Unknown Distance"
```

### Either Type Usage
```python
from pyffect import Either, Right, Left


def divide(numerator: int, denominator: int) -> Either[str, float]:
    try:
        value = numerator / denominator
        return Right(value)
    except:
        return Left('unable to perform the operation.')


firstValue: Either[str, float] = divide(5, 0)
assert firstValue.isLeft
assert firstValue.leftValue == 'unable to perform the operation.'
secondValue: Either[str, float] = divide(5, 2)
assert secondValue.isRight
assert secondValue.rightValue == 2.5

```