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
  global names, adjectives, kobold

  if not names or not adjectives:
    kobold = "<span style='color: coral;'>Out of kobolds!</span><span style='color: coral;'>Please refill.</span>"
  else:
    name = random.choice(names)
    adjective = random.choice(adjectives)
    names.remove(name)
    adjectives.remove(adjective)
    kobold = f"{name} the {adjective}"

  return Redirect("/") if not req.headers.get("HX-Request") else kobold

@rt("/refill", methods=["POST"])
def refill(req):
  global names, adjectives, kobold

  names = DEFAULT_NAMES[:]
  adjectives = DEFAULT_ADJECTIVES[:]
  kobold = ""

  return Redirect("/") if not req.headers.get("HX-Request") else kobold

serve()
