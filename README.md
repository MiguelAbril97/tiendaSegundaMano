Template tag 5:
for empty: muebles/lista
if-else: usuarios/lista
extends: en cada lista
include: en cada lista y principal
comment: index

Operadores logicos 5:
>,==,<, and, or: en productos/lista

Template filters 10:
length: usuarios/lista --> 1
lower,date: productos/producto --> 2
truncatewords: productos/categoria --> 1
linebreaksbr: productos/lista --> 1
default,upper, title: usuarios/producto --> 3
capfirst, cut: muebles/lista -->2