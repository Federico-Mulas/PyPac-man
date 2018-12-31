# Level format

## Structure
The first row it's used to know the dimension of the field in the format **r**x**c**
where:

* **r**: it's the number of rows;
* **c**: it's the number of columns;

then the other rows represent how the filed it's done in particular:

* **\#**: it's used for walls;
* ' ': (a space character) it' used for blanks spots;
* \+: it's used to set the spawn point of the pac-man (only one will be chosen);

## Example
*levels/level1.txt*
```
8x7
#######
#     #
# ### #
#     #
       
# ### #
#  +  #
#######
```
