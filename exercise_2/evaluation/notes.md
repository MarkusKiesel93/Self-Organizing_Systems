# Einleitung

Wahl des 4. Sets, mit den Fitness-functions:
F7, F2, F3

und den Constraints:
C5, C3, C10

# Aufgabenteilung

Alex:  Schwefel function (F2) && π₯ > π¦ + 20 ππ π₯ < π¦ β 20 (C3)
Markus:  Boothβs function (F7) &&  π₯2 + π¦2 < 9000 πππ π₯2 + π¦2 > 4000 (C5)
Laurenz: Shubert function (F3) && tan(π₯ π¦) < 1 (C10)

Implemetierung einer eigenen Penalty-Funktion fΓΌr Constraint-handeling und vergleiche penalty function mit der bereits implementierten rejection strategy.

# Experiment automation (Java project)

* openJDK 11 used
* manually add /path/to/NetLogo/lib/app/netlogo-6.3.0.jar library
* add the following VM options: -Xmx1024m -Dfile.encoding=UTF-8 -Djava.library.path=./lib

# TODO:

- show disadvantage of penalty method (optimum can be in restricted area)

# Visualization

- Open to discussion

# Hypothesis

- A small speed limit decreases convergence rate but increases success changes for convergence
- A weaker swarm coupling decreases convergence speed, because less individuals are in a good area, but also decreases the likelihood of getting caught in local minima
- A high paricle inertia allows the swarm to overcome a local minima by overshooting the target
- The penalty method allows for the swarm to tunnel through forbidden areas and therefore better find optima at the constrain boundaries