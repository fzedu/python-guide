---
layout: default
title: Преобразование типов данных 
published: false
mathjax: true
---

# Преобразование типов данных

## Булевы

Для приведения других типов данных к булеву существует функция `bool()`, работающая по следующим соглашениям:

* строки:
```python
# пустая строка - False
bool("") == False
# непустая строка - True
bool("qwerty") == True
```

* числа:
```python
# нулевое число - False
bool(0.0) == False
# ненулевое число (включая отрицательные) - True
bool(15) == bool(-15) == True
```

* списки и кортежи:
```python
# пустой список/кортеж - False
bool([]) == False
# непустой список/кортеж (даже если элемент является пустым списком/кортежем) - True
bool(["hi"]) == bool([[]]) == True
```

* функции:
```python
# всегда True
bool(print) == True
```

Булев тип приводится к следующим типам данных:

* к строке:
```python
str(True) == "True"
str(False) == "False"
```

* к числам:
```python
# True
int(True) == 1
float(True) == 1.0
complex(True) == 1 + 0j
# False
int(False) == 0
float(False) == 0.0
complex(False) == 0j
```