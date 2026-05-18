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

    nodes = {
        "ability_motivation": "Ability/Motivation",
        "family_ses": "Family Socio-Economic Status",
        "education": "Formal Education",
        "parents_education": "Parents Education Level",
        "family_wealth": "Family Wealtth",
        "income": "Income",
        "profess_network": "Access to Professional Network",
        "survey_participation": "Survey participation",
        "occupation": "Occupation",
        "test_scores": "Test Scores",
        "location": "Location",
        "work_experience": "Years of Work Experience",
        "field_of_study": "Field of Study",
    }

    g.add_nodes_from(nodes.keys())

    # Add directed edges
    edges = [
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
            "education",
            {
                "rationale": (
                    "Educated parents are more likely to value, support, and finance their children's education"
                )
            },
        ),
        (
            "family_wealth",
            "education",
            {
                "rationale": (
                    "Wealthier families can better afford tuition, books, relocation, "
                    "and reduced financial pressure during study"
                )
            },
        ),
        (
            "family_wealth",
            "income",
            {
                "rationale": (
                    "Family wealth can directly influence adult income through inheritance, "
                    "financial safety nets, and investment opportunities"
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
            "education",
            {
                "rationale": (
                    "More motivated and academically capable individuals are more likely "
                    "to pursue and complete higher levels of education"
                )
            },
        ),
        (
            "ability_motivation",
            "income",
            {
                "rationale": (
                    "Ability and motivation can independently improve labor productivity "
                    "and career success beyond formal education"
                )
            },
        ),
        (
            "test_scores",
            "education",
            {
                "rationale": (
                    "Strong academic performance increases admission chances and progression "
                    "through educational systems"
                )
            },
        ),
        (
            "test_scores",
            "income",
            {
                "rationale": (
                    "Test scores may proxy for cognitive skills valued in the labor market"
                )
            },
        ),
        # --- Geography and local opportunity structure ---
        (
            "location",
            "education",
            {
                "rationale": (
                    "Location affects access to schools, universities, educational quality, "
                    "and educational policy environments"
                )
            },
        ),
        (
            "location",
            "income",
            {
                "rationale": (
                    "Regional labor markets differ in wages, industry composition, "
                    "and economic opportunity"
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
        # --- Education pathways and labor market mechanisms ---
        (
            "education",
            "field_of_study",
            {
                "rationale": (
                    "Individuals typically select a field of study within the broader educational system"
                )
            },
        ),
        (
            "education",
            "occupation",
            {
                "rationale": (
                    "Educational attainment influences access to occupations requiring credentials "
                    "or specialized knowledge"
                )
            },
        ),
        (
            "education",
            "profess_network",
            {
                "rationale": (
                    "Educational institutions provide access to alumni, peers, mentors, "
                    "and professional networking opportunities"
                )
            },
        ),
        (
            "education",
            "work_experience",
            {
                "rationale": (
                    "Education affects career timing, labor market entry, "
                    "and opportunities for skill accumulation"
                )
            },
        ),
        (
            "education",
            "income",
            {
                "rationale": (
                    "Formal education increases human capital, credentials, "
                    "and access to higher-paying jobs"
                )
            },
        ),
        (
            "field_of_study",
            "occupation",
            {
                "rationale": (
                    "Field of study strongly influences career specialization and occupational sorting"
                )
            },
        ),
        (
            "field_of_study",
            "income",
            {
                "rationale": (
                    "Different academic disciplines are associated with different average earnings"
                )
            },
        ),
        (
            "profess_network",
            "occupation",
            {
                "rationale": (
                    "Professional networks help individuals obtain information, referrals, "
                    "and job opportunities"
                )
            },
        ),
        (
            "profess_network",
            "income",
            {
                "rationale": (
                    "Networks can improve promotion prospects, bargaining power, "
                    "and access to higher-paying positions"
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
        (
            "work_experience",
            "income",
            {
                "rationale": (
                    "Additional years of work experience increase skills, productivity, "
                    "and wages over time"
                )
            },
        ),
        # --- Survey selection mechanisms ---
        (
            "education",
            "survey_participation",
            {
                "rationale": (
                    "Educational attainment may affect willingness or ability "
                    "to participate in surveys"
                )
            },
        ),
        (
            "income",
            "survey_participation",
            {
                "rationale": (
                    "Income may influence survey participation through time availability, "
                    "trust, or accessibility"
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
    ]

    g.add_edges_from(edges)

    nx.set_node_attributes(g, nodes, "label")

    # Verify DAG
    print("Is DAG:", nx.is_directed_acyclic_graph(g))

    pgmpy_dag = DAG(g)
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
    include_var__family_ses = mo.ui.checkbox(label="Family Socio-Economic Status")
    include_var__test_scores = mo.ui.checkbox(label="Test Scores")

    mo.vstack(
        [
            mo.md("## Variables to Include in Model"),
            include_var__family_ses,
            include_var__test_scores,
        ]
    )
    return include_var__family_ses, include_var__test_scores


@app.cell(column=2, hide_code=True)
def _(mo):
    mo.md(r"""
    # Results
    """)
    return


@app.cell(hide_code=True)
def _(g, include_var__family_ses, include_var__test_scores, json, mo):
    nodes_included_in_model = set()
    for vbl_name, checkbox in (
        ("family_ses", include_var__family_ses),
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

                'color': '#f3f4f6',

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
                 'color': '#f3f4f6',
 
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

    mo.iframe(html, height="600px")
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
