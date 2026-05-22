import marimo

__generated_with = "0.23.6"
app = marimo.App(width="columns")


@app.cell(column=0, hide_code=True)
def _(mo):
    mo.md(r"""
    # Setup
    """)
    return


@app.cell
def _():
    import json

    import marimo as mo
    import networkx as nx
    from pgmpy.base import DAG

    return DAG, json, mo, nx


@app.cell
def _(DAG, nx):
    g = nx.DiGraph()

    ## TODO ##
    # NEED TO ADD scholarship -> education_level

    nodes = {
        "ability_motivation": "Ability/Motivation",
        "education_level": "Formal Education Level Attained",
        "education_institution": "Most Recent Education Institution Attended",
        "parents_education": "Parents Education Level",
        "family_wealth": "Family Wealtth",
        "income": "Income",
        "profess_network": "Access to Professional Network",
        "survey_participation": "Survey participation",
        "occupation": "Occupation",
        "test_scores": "Most Recent Test Scores",
        "location": "Location",
        "scholarship": "Received scholarship for most recent study",
    }

    g.add_nodes_from(nodes.keys())

    # Add directed edges
    edges = [
        # --- Family background ---
        (
            "parents_education",
            "family_wealth",
            {
                "rationale": (
                    "Higher parental education is often associated with greater lifetime wealth accumulation"
                )
            },
        ),
        (
            "parents_education",
            "education_level",
            {
                "rationale": (
                    "Educated parents are more likely to value, support, and finance their children's education"
                )
            },
        ),
        (
            "parents_education",
            "education_institution",
            {
                "rationale": (
                    "Educated parents are more likely to prioritize academics differently, have preferences for specific schools, and are likely to be more comfortable and experienced navigating admissions processes."
                )
            },
        ),
        (
            "family_wealth",
            "education_level",
            {
                "rationale": (
                    "Wealthier families can better afford tuition, books, relocation, and reduced financial pressure during study"
                )
            },
        ),
        (
            "family_wealth",
            "education_institution",
            {
                "rationale": (
                    "Wealthier families can better access prestigious, distant, or higher-quality institutions"
                )
            },
        ),
        (
            "family_wealth",
            "income",
            {
                "rationale": (
                    "Family wealth can directly influence adult income through inheritance, financial safety nets, and investment opportunities"
                )
            },
        ),
        (
            "family_wealth",
            "scholarship",
            {
                "rationale": (
                    "Poor families are eligible for needs-based scholarships"
                )
            },
        ),
        # --- Ability and academic preparation ---
        (
            "ability_motivation",
            "test_scores",
            {
                "rationale": (
                    "Innate ability and motivation strongly influence academic test performance"
                )
            },
        ),
        (
            "ability_motivation",
            "scholarship",
            {
                "rationale": (
                    "More talented and motivated students are more likely to chase scholarships"
                )
            },
        ),
        (
            "ability_motivation",
            "education_level",
            {
                "rationale": (
                    "More motivated and academically capable individuals are more likely to pursue and complete higher levels of education"
                )
            },
        ),
        (
            "ability_motivation",
            "education_institution",
            {
                "rationale": (
                    "More capable or motivated individuals may gain admission to better institutions will likely prioritize different schools"
                )
            },
        ),
        (
            "ability_motivation",
            "income",
            {
                "rationale": (
                    "Ability and motivation can independently improve labor productivity and career success beyond formal education"
                )
            },
        ),
        (
            "test_scores",
            "scholarship",
            {
                "rationale": (
                    "High academic achievement is required for merit-based scholarships"
                )
            },
        ),
        # --- Geography and local opportunity structure ---
        (
            "location",
            "education_level",
            {
                "rationale": (
                    "Location affects access to schools, universities, educational quality, and educational policy environments"
                )
            },
        ),
        (
            "location",
            "education_institution",
            {
                "rationale": (
                    "Location shapes which institutions are available and how costly it is to attend them"
                )
            },
        ),
        (
            "location",
            "income",
            {
                "rationale": (
                    "Regional labor markets differ in wages, industry composition, and economic opportunity"
                )
            },
        ),
        (
            "location",
            "occupation",
            {
                "rationale": (
                    "Occupational opportunities vary substantially across regions and cities"
                )
            },
        ),
        (
            "location",
            "survey_participation",
            {
                "rationale": (
                    "Survey accessibility and response rates often vary by geographic region"
                )
            },
        ),
        # --- Education pathways and labor market mechanisms ---
        (
            "education_level",
            "occupation",
            {
                "rationale": (
                    "Educational attainment influences access to occupations requiring credentials or specialized knowledge"
                )
            },
        ),
        (
            "education_level",
            "profess_network",
            {
                "rationale": (
                    "Longer educational exposure can expand access to peers, mentors, and alumni networks"
                )
            },
        ),
        (
            "education_level",
            "income",
            {
                "rationale": (
                    "Formal education increases access to higher-paying jobs"
                )
            },
        ),
        (
            "education_level",
            "survey_participation",
            {
                "rationale": (
                    "Educational attainment may affect willingness or ability to participate in surveys"
                )
            },
        ),
        (
            "education_institution",
            "education_level",
            {
                "rationale": (
                    "Schools typically teach only at a specific education level (e.g. tertiary)"
                )
            },
        ),
        (
            "education_institution",
            "occupation",
            {
                "rationale": (
                    "Institution quality, prestige, and recruiting pipelines can shape occupational sorting"
                )
            },
        ),
        (
            "education_institution",
            "profess_network",
            {
                "rationale": (
                    "Educational institutions provide access to alumni, peers, mentors, and professional networking opportunities"
                )
            },
        ),
        (
            "education_institution",
            "income",
            {
                "rationale": (
                    "Institution quality, reputation, and access to recruiting channels can affect later earnings"
                )
            },
        ),
        # --- Labor-market mediators ---
        (
            "profess_network",
            "occupation",
            {
                "rationale": (
                    "Professional networks help individuals obtain information, referrals, and job opportunities"
                )
            },
        ),
        (
            "profess_network",
            "income",
            {
                "rationale": (
                    "Networks can improve promotion prospects, bargaining power, and access to higher-paying positions"
                )
            },
        ),
        (
            "occupation",
            "income",
            {
                "rationale": (
                    "Occupations differ systematically in compensation and earning potential"
                )
            },
        ),
        # --- Survey selection mechanisms ---
        (
            "income",
            "survey_participation",
            {
                "rationale": (
                    "Income may influence survey participation through time availability, trust, or accessibility"
                )
            },
        ),
    ]

    g.add_edges_from(edges)

    nx.set_node_attributes(g, nodes, "label")

    # Verify DAG
    print("Is DAG:", nx.is_directed_acyclic_graph(g))

    pgmpy_dag = DAG(
        g,
        roles={"exposures": "education_level", "outcomes": "income"},
    )
    return g, pgmpy_dag


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Notes
    """)
    return


@app.cell(column=1, hide_code=True)
def _(mo):
    mo.md(r"""
    # Controls
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    include_var__education_level = mo.ui.checkbox(
        label="Formal Education Level Attained"
    )
    include_var__education_institution = mo.ui.checkbox(
        label="Most Recent Education Institution Attended"
    )
    include_var__parents_education = mo.ui.checkbox(
        label="Parents Education Level"
    )
    include_var__family_wealth = mo.ui.checkbox(label="Family Wealth")
    include_var__income = mo.ui.checkbox(label="Income")
    include_var__profess_network = mo.ui.checkbox(
        label="Access to Professional Network"
    )
    include_var__survey_participation = mo.ui.checkbox(
        label="Survey participation"
    )
    include_var__occupation = mo.ui.checkbox(label="Occupation")
    include_var__test_scores = mo.ui.checkbox(label="Most Recent Test Scores")
    include_var__location = mo.ui.checkbox(label="Location")
    include_var__scholarship = mo.ui.checkbox(
        label="Received scholarship for most recent study"
    )

    mo.vstack(
        [
            mo.md("## Variables to Include in Model"),
            include_var__education_level,
            include_var__education_institution,
            include_var__parents_education,
            include_var__family_wealth,
            include_var__income,
            include_var__profess_network,
            include_var__survey_participation,
            include_var__occupation,
            include_var__test_scores,
            include_var__location,
            include_var__scholarship,
        ]
    )
    return (
        include_var__education_institution,
        include_var__education_level,
        include_var__family_wealth,
        include_var__income,
        include_var__location,
        include_var__occupation,
        include_var__parents_education,
        include_var__profess_network,
        include_var__scholarship,
        include_var__survey_participation,
        include_var__test_scores,
    )


@app.cell
def _(pgmpy_dag):
    import pgmpy
    from pgmpy.identification import Adjustment

    # https://pgmpy.org/examples/Causal_Games.html
    needs_adjustment: bool = Adjustment().validate(pgmpy_dag)
    print(f"Are there any active backdoor paths? {not needs_adjustment}")

    adjusted_graphs, success = Adjustment(variant="all").identify(pgmpy_dag)

    print(f"No. of potential adjustment sets: {len(adjusted_graphs)}")

    all_backdoor_adjustment_sets = [
        str(graph.get_role("adjustment")) for graph in adjusted_graphs
    ]
    print("Possible backdoor adjustment sets:")
    for adjustment_set in all_backdoor_adjustment_sets:
        print(adjustment_set)
    return


@app.cell
def _():
    return


@app.cell(column=2, hide_code=True)
def _(mo):
    mo.md(r"""
    # Results
    """)
    return


@app.cell(hide_code=True)
def _(
    g,
    include_var__education_institution,
    include_var__education_level,
    include_var__family_wealth,
    include_var__income,
    include_var__location,
    include_var__occupation,
    include_var__parents_education,
    include_var__profess_network,
    include_var__scholarship,
    include_var__survey_participation,
    include_var__test_scores,
    json,
    mo,
):
    nodes_included_in_model = set()
    for vbl_name, checkbox in (
        ("education_level", include_var__education_level),
        ("education_institution", include_var__education_institution),
        ("parents_education", include_var__parents_education),
        ("family_wealth", include_var__family_wealth),
        ("income", include_var__income),
        ("profess_network", include_var__profess_network),
        ("survey_participation", include_var__survey_participation),
        ("occupation", include_var__occupation),
        ("test_scores", include_var__test_scores),
        ("location", include_var__location),
        ("scholarship", include_var__scholarship),
    ):
        if checkbox.value:
            nodes_included_in_model.add(vbl_name)

    # Convert to Cytoscape format
    cy_nodes = [
        {
            "data": {
                "id": node,
                "label": g.nodes[node]["label"],
            },
            "classes": "var-in-model"
            if node in nodes_included_in_model
            else "var-not-in-model",
        }
        for node in g.nodes()
    ]

    cy_edges = [
        {
            "data": {
                "source": source,
                "target": target,
                "rationale": g.edges[source, target]["rationale"],
            }
        }
        for source, target in g.edges()
    ]

    elements = cy_nodes + cy_edges

    # ----------------------------
    # HTML + Cytoscape.js
    # ----------------------------
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8"/>

      <script src="https://unpkg.com/cytoscape@3.30.2/dist/cytoscape.min.js"></script>
      <script src="https://unpkg.com/dagre@0.8.5/dist/dagre.min.js"></script>
      <script src="https://unpkg.com/cytoscape-dagre@2.5.0/cytoscape-dagre.js"></script>

      <style>
        html, body {{
          margin: 0;
          padding: 0;
          width: 100%;
          height: 100%;
          overflow: hidden;

          background: #0b1020;
          color: #e5e7eb;

          font-family:
            Inter,
            ui-sans-serif,
            system-ui,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
        }}

        #cy {{
          width: 100%;
          height: 700px;
          background: #0b1020;
        }}
      </style>
    </head>

    <body>
      <div id="cy"></div>

      <script>
        cytoscape.use(cytoscapeDagre);

        const cy = cytoscape({{
          container: document.getElementById('cy'),

          elements: {json.dumps(elements)},

          style: [

            // -------------------------
            // Base node style
            // -------------------------
            {{
              selector: 'node',
              style: {{
                'label': 'data(label)',

                'shape': 'roundrectangle',

                'background-color': '#111827',
                'border-width': 1.5,
                'border-color': '#374151',

                'color': '#ffffff',

                'text-wrap': 'wrap',
                'text-max-width': 140,

                'text-valign': 'center',
                'text-halign': 'center',

                'font-size': 25,
                'font-weight': 500,

                'padding': '14px',

                'width': 'label',
                'height': 'label',

                'transition-property':
                  'background-color border-color opacity',

                'transition-duration': '160ms',
              }}
            }},

            // -------------------------
            // INCLUDED variables
            // -------------------------
            {{
              selector: '.var-in-model',
              style: {{
                'background-color': '#2563eb',
                'border-color': '#93c5fd',
                'border-width': 2.5,

                'color': '#ffffff',

                'opacity': 1,

                'shadow-blur': 18,
                'shadow-color': '#60a5fa',
                'shadow-opacity': 0.35,
              }}
            }},

            // -------------------------
            // NOT included variables
            // -------------------------
            {{
              selector: '.var-not-in-model',
              style: {{
                'opacity': 0.35,
              }}
            }},

            // -------------------------
            // Edges
            // -------------------------
            {{
              selector: 'edge',
              style: {{
                'curve-style': 'bezier',

                'width': 2,

                'line-color': '#6b7280',

                'target-arrow-color': '#ffffff',
                'target-arrow-shape': 'triangle',

                'arrow-scale': 1.1,

                'opacity': 0.75,

                 // hidden by default
                 'label': '',
                 'font-size': 25,
                 'color': '#ffffff',

                 'text-background-color': '#111827',
                 'text-background-opacity': 0.9,
                 'text-background-padding': 6,
                 'text-background-shape': 'roundrectangle',

                 'text-wrap': 'wrap',
                 'text-max-width': 260,
              }}
            }},

             // -------------------------
             // Hovered edges
             // -------------------------
             {{
               selector: 'edge.hover',
               style: {{
                 'label': 'data(rationale)',

                 'line-color': '#93c5fd',
                 'target-arrow-color': '#93c5fd',

                 'width': 3,
                 'z-index': 999,
               }}
             }},

            // -------------------------
            // Hovered nodes
            // -------------------------
            {{
              selector: '.hover',
              style: {{
                'border-color': '#bfdbfe',
                'background-color': '#1f2937',
                    'text-opacity': 1,
                    'opacity': 1,
              }}
            }},

            // -------------------------
            // Faded elements
            // -------------------------
            {{
              selector: '.faded',
              style: {{
                'opacity': 0.12,
              }}
            }}
          ],

          layout: {{
            name: 'dagre',

            rankDir: 'LR',

            spacingFactor: 1.3,

            nodeSep: 60,
            rankSep: 120,
            edgeSep: 20,

            animate: true,
            animationDuration: 450,

            fit: true,
            padding: 40,
          }},

          wheelSensitivity: 0.2,
        }});

        // Initial framing
        cy.fit(40);

        // Hover interactions
        cy.on('mouseover', 'node', (e) => {{
          e.target.addClass('hover');
        }});

        cy.on('mouseout', 'node', (e) => {{
          e.target.removeClass('hover');
        }});

        // Click neighborhood focus
        cy.on('tap', 'node', function(evt) {{
          const node = evt.target;
          const neighborhood = node.closedNeighborhood();

          cy.elements().addClass('faded');
          neighborhood.removeClass('faded');
        }});

        // Reset fade on background tap
        cy.on('tap', function(event) {{
          if (event.target === cy) {{
            cy.elements().removeClass('faded');
          }}
        }});

         // Edge hover interactions
         cy.on('mouseover', 'edge', (e) => {{
           e.target.addClass('hover');
         }});

         cy.on('mouseout', 'edge', (e) => {{
           e.target.removeClass('hover');
         }});
      </script>
    </body>
    </html>
    """

    mo.iframe(html, height="500px")
    return


@app.cell
def _():
    return


@app.cell(column=3, hide_code=True)
def _(mo):
    mo.md(r"""
    # Testable Implications
    """)
    return


@app.cell
def _(pgmpy_dag):
    print(pgmpy_dag.get_independencies())
    return


if __name__ == "__main__":
    app.run()
