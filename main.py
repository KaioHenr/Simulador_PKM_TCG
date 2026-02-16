from decks.froslass import build, NAME
from core.engine import run
from core.report import print_report

ITER = 30
results = run(build, ITER)
print_report(results, ITER, NAME)
