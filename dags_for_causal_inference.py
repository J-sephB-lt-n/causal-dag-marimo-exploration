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

    return json, mo, nx


@app.cell
def _(nx):
    g = nx.DiGraph()

    nodes = {
        "ability_motivation": "Ability/Motivation",
        "family_ses": "Family Socio-Economic Status",
        "education": "Formal Education",
        "income": "Income",
        "profess_network": "Access to Professional Network",
        "survey_participation": "Survey participation",
        "occupation": "Occupation",
        "test_scores": "Test Scores",
    }

    g.add_nodes_from(nodes.keys())

    # Add directed edges
    edges = [
        ("ability_motivation", "education"),
        ("ability_motivation", "test_scores"),
        ("family_ses", "education"),
        ("family_ses", "profess_network"),
        ("education", "occupation"),
        ("education", "profess_network"),
        ("education", "income"),
        ("occupation", "income"),
        ("profess_network", "occupation"),
        ("income", "survey_participation"),
    ]

    g.add_edges_from(edges)

    nx.set_node_attributes(g, nodes, "label")

    # Verify DAG
    print("Is DAG:", nx.is_directed_acyclic_graph(g))
    return (g,)


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
    include_var__ability_motivation = mo.ui.checkbox(label="Ability/Motivation")
    include_var__test_scores = mo.ui.checkbox(label="Test Scores")

    mo.vstack(
        [
            mo.md("## Variables to Include in Model"),
            include_var__ability_motivation,
            include_var__test_scores,
        ]
    )
    return include_var__ability_motivation, include_var__test_scores


@app.cell(column=2, hide_code=True)
def _(mo):
    mo.md(r"""
    # Results
    """)
    return


@app.cell(hide_code=True)
def _(g, include_var__ability_motivation, include_var__test_scores, json, mo):
    nodes_included_in_model = set()
    for vbl_name, checkbox in (
        ("ability_motivation", include_var__ability_motivation),
        ("test_scores", include_var__test_scores),
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

                'color': '#f3f4f6',

                'text-wrap': 'wrap',
                'text-max-width': 140,

                'text-valign': 'center',
                'text-halign': 'center',

                'font-size': 13,
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

                'target-arrow-color': '#6b7280',
                'target-arrow-shape': 'triangle',

                'arrow-scale': 1.1,

                'opacity': 0.75,
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
      </script>
    </body>
    </html>
    """

    mo.iframe(html, height="640px")
    return


@app.cell
def _():
    return


@app.cell(column=3)
def _():
    return


if __name__ == "__main__":
    app.run()
