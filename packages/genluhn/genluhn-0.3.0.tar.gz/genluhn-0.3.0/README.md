# Generalized Luhn algorithm to any numerical base

Luhn algorithm is described in Annex B of [ISO/IEC 7812-1:2017](https://www.iso.org/standard/70484.html). As it is described at [Luhn's Wikipedia page](https://en.wikipedia.org/wiki/Luhn_algorithm), the algorithm is used to compute check digits and check them in identification numbers, like the usually found in credit card numbers. The standard algorithm uses 10 as numeric base for the check digit.

But there are other scenarios, like [nih URIs at IETF RFC 6920](https://datatracker.ietf.org/doc/html/rfc6920#section-7), where the numeric base of the check digit to be computed and validated is 16 (see examples at [section 8.2](https://datatracker.ietf.org/doc/html/rfc6920#section-8.2) of RFC 6920).

This library is just an implementation of the algorithm for any base. There are two methods, `compute` and `validate`, which take as first parameter either an integer, or a string representing the number in the base, or an array of integers, where the value of each position is the corresponding numeric digit. `compute` method computes the check digit, meanwhile `validate` takes the whole identification number, the numerical base and the check digit, and answers either `True` or `False`.

```python
genluhn.compute('5326-9057-e12f-e2b7-4ba0-7c89-2560-a2',16)
# It return 15

genluhn.validate('5326-9057-e12f-e2b7-4ba0-7c89-2560-a2', 16, 15)
# It returns True

genluhn.validate('5326-9057-e12f-e2b7-4ba0-7c89-2560-a2', 16, 14)
# It returns False
```


Accessory methods of this library are `intToDigits`, `strToDigits` and `bytesToDigits`, which are used when either an integer, or a string or a byteslike object have to be translated to a list of digits in the given numerical base.
