from fasthtml.common import *

import random

app, rt = fast_app(
  pico=False,
  default_hdrs=False,
)

def load_data(filepath):
  with open(filepath, encoding='utf-8') as f:
    return [line.strip() for line in f if line.strip()]

DEFAULT_NAMES = load_data("data/names.txt")
DEFAULT_ADJECTIVES = load_data("data/adjectives.txt")

names = DEFAULT_NAMES[:]
adjectives = DEFAULT_ADJECTIVES[:]
kobold = ""
easter_egg_used = False
easter_egg_slot = None
dispense_count = 0


def layout(*content):
  return Html(
    Head(
      Title("Kobold Vending Machine"),
      Meta(charset="UTF-8"),
      Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
      Link(rel="stylesheet", href="assets/styles.css", type="text/css"),
      Script(src="https://unpkg.com/htmx.org@1.9.5", type="text/javascript")
    ),
    Body(*content)
  )

@rt
def index():
  return layout(
    Main(
      Div(
        H1("Kobold Vending Machine", data_name="Kobold Vending Machine",),
        cls="nameplate"
      ),
      Div(
        Span("1GP"),
        cls="coinplate"
      ),
      Form(
        Button(
          Span("Get a kobold", data_name="Get a kobold"), 
          cls="button--dispense", 
          type="submit", 
          hx_post="/dispense", 
          hx_target="#dispenser-slot", 
          hx_swap="innerHTML"
        ),
        action="/dispense",
        method="post",
        style="display: contents;"
      ),
      Div(kobold, cls="dispenser-slot", id="dispenser-slot", aria_live="assertive"),
      cls="machine"
    ),
    Form(
      Button(
        Span("Refill", data_name="Refill"),
        cls="button--refill", 
        type="submit", 
        hx_post="/refill", 
        hx_target="#dispenser-slot", 
        hx_swap="innerHTML"
      ),
      action="/refill", method="post"
    ),
    Footer(
      Div(
        Span("A "),
        A("wee notion", href="https://weenotions.com"),
        Span(" by Paddy Duke"),
        cls="section"
      )
    )
  )

@rt("/dispense", methods=["POST"])
def dispense(req):
  global names, adjectives, kobold, easter_egg_used, easter_egg_slot, dispense_count

  if not easter_egg_used and dispense_count == easter_egg_slot:
    kobold = "Kronk the lever puller"
    easter_egg_used = True
    if names: names.pop()
    if adjectives: adjectives.pop()
    dispense_count += 1

  elif names and adjectives:
    name = random.choice(names)
    adjective = random.choice(adjectives)
    names.remove(name)
    adjectives.remove(adjective)
    kobold = f"{name} the {adjective}"
    dispense_count += 1

  else:
    kobold = "<span style='color: coral;'>Out of kobolds!</span><span style='color: coral;'>Please refill.</span>"

  return Redirect("/") if not req.headers.get("HX-Request") else kobold

@rt("/refill", methods=["POST"])
def refill(req):
  global names, adjectives, kobold, easter_egg_slot, easter_egg_used, dispense_count

  names = DEFAULT_NAMES[:]
  adjectives = DEFAULT_ADJECTIVES[:]
  kobold = ""

  total_dispenses = min(len(names), len(adjectives))
  easter_egg_slot = random.randint(0, total_dispenses - 1)
  easter_egg_used = False
  dispense_count = 0

  return Redirect("/") if not req.headers.get("HX-Request") else kobold

serve()
