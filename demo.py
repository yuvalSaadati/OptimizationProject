from lpscheduler import *

# set up problem space
who  = ['Math Teacher1', 'Math Teacher2', 'English Teacher1','English Teacher2',
        'Geography Teacher', 'Sciences Teacher', 'Sport Teacher']
when = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri']
what = ['Math', 'English', 'Geography', 'Sciences', 'Sport','free']

# initialize scheduler
s = Scheduler(who, when, what)

# constraint: every teacher teach his subject
for _what in what:
    for _who in who:
        if _what not in _who and _what != 'free':
            cons = Constraint(sum(s(_who, _when, _what) for _when in when), '=', 0)
            s.addcons(cons)


# There will be two math classes- on Sunday and Tuesday
for _what in what:
    for _who in who:
        if _what in _who and _what != 'free' and _what == "Math":
            cons = Constraint(sum(s(_who, _when, _what) for _when in ['Sun', 'Tue']), '=', 1)
            s.addcons(cons)
            cons = Constraint(sum(s(_who, _when, _what) for _when in [ 'Mon', 'Wed', 'Thu', 'Fri']), '=', 0)
            s.addcons(cons)

#constraint: MathTeacher1 needs Sunday, Mondays off
cons = Constraint(s('Math Teacher1', 'Sun', 'free'), '=', 1)
s.addcons(cons)

# There will be two English classes- on Sunday and Tuesday
for _what in what:
    for _who in who:
        if _what in _who and _what != 'free' and _what == "English":
            cons = Constraint(sum(s(_who, _when, _what) for _when in ['Sun', 'Tue']), '=', 1)
            s.addcons(cons)
            cons = Constraint(sum(s(_who, _when, _what) for _when in [ 'Mon', 'Wed', 'Thu', 'Fri']), '=', 0)
            s.addcons(cons)

#constraint: English Teacher1 needs Sunday, Mondays off
cons = Constraint(s('English Teacher1', 'Sun', 'free'), '=', 1)
s.addcons(cons)
#constraint: English Teacher2 needs Tuesday, Mondays off
cons = Constraint(s('English Teacher2', 'Tue', 'free'), '=', 1)
s.addcons(cons)

# There will be at least one Geography classes- on Monday
cons = Constraint(s('Geography Teacher', 'Mon', 'Geography'), '>=', 1)
s.addcons(cons)
# There will be at least one Geography classes- on Friday
cons = Constraint(s('Sport Teacher', 'Fri', 'Sport'), '>=', 1)
s.addcons(cons)

# There will be Sciences classes only on Wednesday only
cons = Constraint(s('Sciences Teacher', 'Wed', 'Sciences'), '=', 1)
s.addcons(cons)
for _what in what:
    for _who in who:
        if _what == 'Sciences' and _what != 'free':
            cons = Constraint(sum(s(_who, _when, _what) for _when in  ['Sun', 'Mon', 'Tue', 'Thu', 'Fri']), '=', 0)
            s.addcons(cons)
# randomize cost to sample solution space
s.setrandcost()

# run solver and show solution
options = {'LPX_K_MSGLEV': 0}  # suppress GLPK output
t = s.solve(**options)
s.show(t)