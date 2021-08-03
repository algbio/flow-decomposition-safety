# flow decomposition safety

## run safety algorithm

```bash
python -m src.scripts.main -i {path/to/input/file} -o {path/to/output/file} -m {optional}
```

## run tests

```bash
python -m unittest discover
```



..........
The current README does not allow an external user to run the code and the experiments:

- This project has dependencies: this can be solved by creating a "requirements.txt" and then put a README instruction
`pip install -r requirements.txt` (see https://realpython.com/lessons/using-requirement-files/ for example, also it is
  not a good practice to put in the requirements all the packages in the pip freeze but only the ones
  required by the project, in this case I think is networkx,pandas,numpy with the corresponding versions)
  
- The current snakefile has a rule to run catfish but there are no README instructions on how and where to install it:
It is not necessary to repeat catfish instructions here, but to give the corresponding "links" to catfish install
instructions.