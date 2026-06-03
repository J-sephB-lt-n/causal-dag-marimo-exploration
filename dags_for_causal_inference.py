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

    import altair as alt
    import marimo as mo
    import networkx as nx
    import numpy as np
    import polars as pl
    import xgboost as xgb
    from scipy.special import softmax
    from scipy.stats import truncnorm
    from pgmpy.base import DAG

    return DAG, alt, json, mo, np, nx, pl, softmax, truncnorm, xgb


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
        (
            "scholarship",
            "education_level",
            {
                "rationale": (
                    "Scholarships increase ease of access to formal education"
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
    include_var__education_institution = mo.ui.checkbox(
        label="Most Recent Education Institution Attended"
    )
    include_var__parents_education = mo.ui.checkbox(
        label="Parents Education Level"
    )
    include_var__family_wealth = mo.ui.checkbox(label="Family Wealth")
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
            include_var__education_institution,
            include_var__parents_education,
            include_var__family_wealth,
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
        include_var__family_wealth,
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
    include_var__family_wealth,
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
        ("education_institution", include_var__education_institution),
        ("parents_education", include_var__parents_education),
        ("family_wealth", include_var__family_wealth),
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
def _(mo):
    run_model_simulations = mo.ui.run_button(label="Run model simulations")
    n_samples = mo.ui.number(
        start=1, stop=100_000, value=999, label="Number of samples"
    )
    n_simulations = mo.ui.number(
        start=1, stop=100_000, value=50, label="Number of simulations"
    )
    mo.vstack(
        [
            n_samples,
            n_simulations,
            run_model_simulations,
        ]
    )
    return n_samples, n_simulations, run_model_simulations


@app.cell(hide_code=True)
def _(
    EDUCATION_LEVELS,
    alt,
    mo,
    n_samples,
    n_simulations,
    pl,
    run_model_simulations,
    simulate_dag,
    xgb,
):
    mo.stop(not run_model_simulations.value)

    sim_model_data = simulate_dag(
        n=n_samples.value,
    )

    mean_income_per_education_level = {
        education_level: []  # 1 value stored for each simulation
        for education_level in EDUCATION_LEVELS
    }

    for i in mo.status.progress_bar(
        range(n_simulations.value), title="Running modelling simulations"
    ):
        for education_level in EDUCATION_LEVELS:
            simdata: pl.DataFrame = simulate_dag(
                n=n_samples.value,
                education_level=education_level,
                seed=i,
            )
            mean_income_per_education_level[education_level].append(
                simdata["income"].mean()
            )

        model = xgb.XGBRegressor(
            tree_method="hist",
            enable_categorical=True,
        )

    plot_df = pl.DataFrame(
        [
            {"education_level": level, "mean_income": value}
            for level, values in mean_income_per_education_level.items()
            for value in values
        ]
    )

    simbase = alt.Chart(plot_df).encode(
        x=alt.X(
            "mean_income:Q",
            bin=alt.Bin(maxbins=100),
            title="Mean income",
        ),
        y=alt.Y("count():Q", title="Simulations"),
    )

    hist = simbase.mark_bar()

    mean_rule = (
        alt.Chart(plot_df)
        .transform_joinaggregate(
            education_mean="mean(mean_income)",
            groupby=["education_level"],
        )
        .mark_rule(strokeWidth=2)
        .encode(
            x=alt.X("education_mean:Q", title="Mean income"),
            tooltip=[
                "education_level:N",
                alt.Tooltip("education_mean:Q", format=",.0f"),
            ],
        )
    )

    simchart = (
        (hist + mean_rule)
        .properties(
            width=900,
            height=60,
        )
        .facet(
            row=alt.Row(
                "education_level:N",
                title=None,
                sort=list(mean_income_per_education_level.keys()),
            )
        )
        .resolve_scale(x="shared", y="independent")
    )

    mo.ui.altair_chart(simchart)
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


@app.cell
def _(simulate_dag):
    sim_data = simulate_dag(n=10_000, seed=420)
    sim_data
    return (sim_data,)


@app.cell
def _(alt, mo, pl, sim_data):
    r = sim_data.select(pl.corr("family_wealth", "test_scores")).item()

    base = alt.Chart(sim_data).encode(
        x=alt.X(
            "family_wealth:Q",
            scale=alt.Scale(type="log"),
            title="Family Wealth (log scale)",
        ),
        y=alt.Y("test_scores:Q", title="Test Scores"),
    )

    chart = (
        base.mark_circle(size=10, opacity=0.4)
        + base.transform_regression("family_wealth", "test_scores").mark_line(
            strokeWidth=3
        )
    ).properties(
        width=700,
        height=450,
        title=f"Family Wealth vs Test Scores (r = {r:.3f})",
    )

    mo.ui.altair_chart(chart)
    return


@app.cell
def _(pl, sim_data):
    (
        sim_data.group_by("parents_education")
        .agg(
            percent_scholarship=pl.col("scholarship").mean() * 100,
            percent_no_scholarship=(~pl.col("scholarship")).mean() * 100,
        )
        .sort("parents_education")
    )
    return


@app.cell
def _(pl, sim_data):
    (
        sim_data.group_by("parents_education")
        .agg(
            percent_scholarship=pl.col("scholarship").mean() * 100,
            percent_no_scholarship=(~pl.col("scholarship")).mean() * 100,
        )
        .sort("parents_education")
    )
    return


@app.cell(column=4, hide_code=True)
def _(mo):
    mo.md(r"""
    # Internals
    """)
    return


@app.cell
def _(np, pl, softmax, truncnorm):
    """
    Simulate data from the education-income causal DAG using ancestral sampling
    with numpy/scipy.

    All monetary values are in ZAR (South African Rand).
    Income is monthly. Family wealth is total household net worth (stock).

    Usage
    -----
        from data_gen_func import simulate_dag

        # Observational sample
        df = simulate_dag(n=5_000)

        # Interventional: do(education_level='3-tertiary-undergrad')
        df_do = simulate_dag(n=5_000, education_level='3-tertiary-undergrad')
    """

    # ---------------------------------------------------------------------------
    # Constants
    # ---------------------------------------------------------------------------

    PROVINCES = [
        "Gauteng",
        "KwaZulu-Natal",
        "Western Cape",
        "Eastern Cape",
        "Limpopo",
        "Mpumalanga",
        "North West",
        "Free State",
        "Northern Cape",
    ]

    PROVINCE_WEIGHTS = np.array(
        [0.26, 0.20, 0.12, 0.11, 0.10, 0.08, 0.07, 0.05, 0.02]
    )
    PROVINCE_WEIGHTS = PROVINCE_WEIGHTS / PROVINCE_WEIGHTS.sum()

    PROVINCE_WAGE_SCALAR = np.array(
        [
            1.35,  # Gauteng
            0.95,  # KwaZulu-Natal
            1.25,  # Western Cape
            0.80,  # Eastern Cape
            0.75,  # Limpopo
            0.85,  # Mpumalanga
            0.82,  # North West
            0.83,  # Free State
            0.88,  # Northern Cape
        ]
    )

    # 1 = rural, 0 = urban
    PROVINCE_IS_RURAL = np.array([0, 0, 0, 1, 1, 1, 1, 0, 1], dtype=float)

    EDUCATION_LEVELS = [
        "0-no-formal-education",
        "1-primary",
        "2-secondary",
        "3-tertiary-undergrad",
        "4-tertiary-masters",
        "5-tertiary-phd",
    ]

    INSTITUTION_LEVELS = [
        "none",
        "community_college",
        "university",
        "elite_university",
    ]

    OCCUPATIONS = ["unemployed", "manual", "service", "professional", "executive"]

    PARENTS_EDU_PROBS = np.array([0.08, 0.17, 0.45, 0.22, 0.06, 0.02])

    # LogNormal (mu, sigma) for family wealth by parents_education index
    WEALTH_MU = np.array([8.8, 9.5, 10.3, 11.5, 12.4, 13.0])
    WEALTH_SIGMA = np.array([1.2, 1.1, 1.0, 0.9, 0.8, 0.7])

    # Monthly income log-means by occupation index
    OCCUPATION_LOG_MU = np.log(
        np.array([3_000, 10_000, 15_000, 30_000, 100_000], dtype=float)
    )


    # ---------------------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------------------


    def _sigmoid(x: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))


    def _categorical(rng: np.random.Generator, probs: np.ndarray) -> np.ndarray:
        """Row-wise categorical draw from a (n, k) probability matrix."""
        cumulative = probs.cumsum(axis=1)
        u = rng.random((len(probs), 1))
        return (u > cumulative).sum(axis=1).astype(int)


    # ---------------------------------------------------------------------------
    # Main simulation function
    # ---------------------------------------------------------------------------


    def simulate_dag(
        n: int,
        education_level: str | None = None,
        seed: int = 42,
    ) -> pl.DataFrame:
        """
        Simulate n observations from the education-income causal DAG via
        ancestral sampling.

        Parameters
        ----------
        n : int
            Number of samples to generate.
        education_level : str or None
            Causal intervention do(education_level=e). Must be one of
            EDUCATION_LEVELS. When set, education_level is fixed for all
            observations rather than sampled from its observational distribution.
        seed : int
            Random seed for reproducibility.

        Returns
        -------
        pl.DataFrame
        """
        if education_level is not None and education_level not in EDUCATION_LEVELS:
            raise ValueError(
                f"education_level must be one of {EDUCATION_LEVELS}, got '{education_level}'"
            )

        rng = np.random.default_rng(seed)

        # ------------------------------------------------------------------
        # 1. ability_motivation  ~  N(0, 1)
        # ------------------------------------------------------------------
        ability = rng.standard_normal(n)

        # ------------------------------------------------------------------
        # 2. location  ~  Categorical(province_weights)
        # ------------------------------------------------------------------
        location_idx = rng.choice(len(PROVINCES), size=n, p=PROVINCE_WEIGHTS)
        is_rural = PROVINCE_IS_RURAL[location_idx]
        wage_scalar = PROVINCE_WAGE_SCALAR[location_idx]

        # ------------------------------------------------------------------
        # 3. parents_education  ~  Categorical(SA marginals)
        # ------------------------------------------------------------------
        parents_edu_idx = rng.choice(
            len(EDUCATION_LEVELS), size=n, p=PARENTS_EDU_PROBS
        )

        # ------------------------------------------------------------------
        # 4. family_wealth  ~  LogNormal(mu[parents_edu], sigma[parents_edu])
        # ------------------------------------------------------------------
        wealth_mu_vec = WEALTH_MU[parents_edu_idx]
        wealth_sigma_vec = WEALTH_SIGMA[parents_edu_idx]
        family_wealth = rng.lognormal(mean=wealth_mu_vec, sigma=wealth_sigma_vec)

        log_wealth = np.log(family_wealth)
        log_wealth_scaled = (log_wealth - log_wealth.mean()) / (
            log_wealth.std() + 1e-8
        )

        # ------------------------------------------------------------------
        # 5. test_scores  ~  TruncatedNormal(50 + 15*ability, 15) in [0, 100]
        # ------------------------------------------------------------------
        ts_mu = 50.0 + 15.0 * ability
        ts_sigma = 15.0
        a_clip = (0.0 - ts_mu) / ts_sigma
        b_clip = (100.0 - ts_mu) / ts_sigma
        test_scores = truncnorm.rvs(
            a_clip,
            b_clip,
            loc=ts_mu,
            scale=ts_sigma,
            random_state=rng.integers(2**31),
        )

        # ------------------------------------------------------------------
        # 6. scholarship  ~  Bernoulli(sigmoid(logit))
        # ------------------------------------------------------------------
        test_scores_scaled = (test_scores - 50.0) / 15.0
        scholarship_logit = (
            -3.8
            - 0.8 * log_wealth_scaled
            + 0.6 * ability
            + 0.8 * test_scores_scaled
        )
        scholarship = (rng.random(n) < _sigmoid(scholarship_logit)).astype(float)

        # ------------------------------------------------------------------
        # 7. education_institution  ~  Categorical(softmax(logits))
        #    0=none, 1=community_college, 2=university, 3=elite_university
        # ------------------------------------------------------------------
        parents_edu_f = parents_edu_idx.astype(float)

        inst_logits = np.column_stack(
            [
                np.zeros(n),
                1.5
                + 0.3 * ability
                + 0.2 * parents_edu_f
                + 0.3 * log_wealth_scaled
                - 0.5 * is_rural,
                -0.5
                + 0.8 * ability
                + 0.6 * parents_edu_f
                + 0.6 * log_wealth_scaled
                - 0.8 * is_rural,
                -3.0
                + 1.2 * ability
                + 0.8 * parents_edu_f
                + 1.0 * log_wealth_scaled
                - 1.2 * is_rural,
            ]
        )
        inst_probs = softmax(inst_logits, axis=1)
        inst_idx = _categorical(rng, inst_probs)

        # ------------------------------------------------------------------
        # 8. education_level  ~  Categorical(softmax(logits))  OR  do()
        # ------------------------------------------------------------------
        inst_f = inst_idx.astype(float)
        is_univ_or_elite = (inst_idx >= 2).astype(float)
        is_elite = (inst_idx == 3).astype(float)

        if education_level is not None:
            edu_idx = np.full(
                n, EDUCATION_LEVELS.index(education_level), dtype=int
            )
        else:
            edu_logits = np.column_stack(
                [
                    np.zeros(n),
                    0.5 + 0.2 * parents_edu_f + 0.1 * ability,
                    2.0
                    + 0.4 * parents_edu_f
                    + 0.3 * ability
                    + 0.3 * log_wealth_scaled
                    - 0.3 * is_rural,
                    0.0
                    + 0.7 * parents_edu_f
                    + 0.8 * ability
                    + 0.7 * log_wealth_scaled
                    - 0.5 * is_rural
                    + 1.5 * is_univ_or_elite
                    + 0.8 * scholarship,
                    -2.0
                    + 0.6 * parents_edu_f
                    + 0.9 * ability
                    + 0.6 * log_wealth_scaled
                    - 0.6 * is_rural
                    + 1.2 * is_elite
                    + 0.5 * scholarship,
                    -4.0
                    + 0.5 * parents_edu_f
                    + 1.0 * ability
                    + 0.5 * log_wealth_scaled
                    - 0.8 * is_rural
                    + 1.0 * is_elite
                    + 0.4 * scholarship,
                ]
            )
            edu_probs = softmax(edu_logits, axis=1)
            edu_idx = _categorical(rng, edu_probs)

        # ------------------------------------------------------------------
        # 9. profess_network  ~  Beta(alpha, beta)
        #    mu = sigmoid(-3 + 0.7*edu + 0.6*inst), kappa=6
        # ------------------------------------------------------------------
        edu_f = edu_idx.astype(float)
        network_mu = _sigmoid(-3.0 + 0.7 * edu_f + 0.6 * inst_f)
        kappa = 6.0
        net_alpha = np.clip(network_mu * kappa, 0.01, None)
        net_beta = np.clip((1.0 - network_mu) * kappa, 0.01, None)
        profess_network = rng.beta(net_alpha, net_beta)

        # ------------------------------------------------------------------
        # 10. occupation  ~  Categorical(softmax(logits))
        # ------------------------------------------------------------------
        occ_logits = np.column_stack(
            [
                np.zeros(n),
                1.5 + 0.2 * edu_f - 0.3 * profess_network + 0.3 * is_rural,
                1.0 + 0.4 * edu_f + 0.4 * profess_network - 0.2 * is_rural,
                -2.0
                + 1.0 * edu_f
                + 0.8 * profess_network
                + 0.6 * inst_f
                - 0.4 * is_rural,
                -5.0
                + 0.8 * edu_f
                + 1.2 * profess_network
                + 1.0 * inst_f
                - 0.3 * is_rural,
            ]
        )
        occ_probs = softmax(occ_logits, axis=1)
        occ_idx = _categorical(rng, occ_probs)

        # ------------------------------------------------------------------
        # 11. income  ~  LogNormal(log_mu, sigma)  monthly ZAR
        # ------------------------------------------------------------------
        occ_base = OCCUPATION_LOG_MU[occ_idx]
        income_log_mu = (
            occ_base
            + 0.15 * edu_f
            + 0.10 * inst_f
            + 0.20 * profess_network
            + 0.05 * log_wealth_scaled
            + 0.10 * ability
            + np.log(wage_scalar)
        )
        income = rng.lognormal(mean=income_log_mu, sigma=2)

        # ------------------------------------------------------------------
        # 12. survey_participation  ~  Bernoulli(sigmoid(logit))
        # ------------------------------------------------------------------
        log_income = np.log(income)
        log_income_scaled = (log_income - log_income.mean()) / (
            log_income.std() + 1e-8
        )
        survey_logit = (
            -1.5 + 0.3 * edu_f + 0.2 * log_income_scaled - 0.4 * is_rural
        )
        survey_participation = rng.random(n) < _sigmoid(survey_logit)

        # ------------------------------------------------------------------
        # Assemble Polars DataFrame
        # ------------------------------------------------------------------
        df = pl.DataFrame(
            {
                "ability_motivation": ability,
                "location": [PROVINCES[i] for i in location_idx],
                "parents_education": [
                    EDUCATION_LEVELS[i] for i in parents_edu_idx
                ],
                "family_wealth": family_wealth,
                "test_scores": test_scores,
                "scholarship": scholarship.astype(bool),
                "education_institution": [INSTITUTION_LEVELS[i] for i in inst_idx],
                "education_level": [EDUCATION_LEVELS[i] for i in edu_idx],
                "profess_network": profess_network,
                "occupation": [OCCUPATIONS[i] for i in occ_idx],
                "income": income,
                "survey_participation": survey_participation,
            }
        )

        df = df.with_columns(
            [
                pl.col("location").cast(pl.Enum(PROVINCES)),
                pl.col("parents_education").cast(pl.Enum(EDUCATION_LEVELS)),
                pl.col("education_institution").cast(pl.Enum(INSTITUTION_LEVELS)),
                pl.col("education_level").cast(pl.Enum(EDUCATION_LEVELS)),
                pl.col("occupation").cast(pl.Enum(OCCUPATIONS)),
            ]
        )

        return df

    return EDUCATION_LEVELS, simulate_dag


if __name__ == "__main__":
    app.run()
