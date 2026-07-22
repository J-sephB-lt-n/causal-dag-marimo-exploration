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
    from typing import Final, Literal

    import altair as alt
    import marimo as mo
    import networkx as nx
    import numpy as np
    import polars as pl
    import xgboost as xgb
    from scipy.special import softmax
    from scipy.stats import gaussian_kde, truncnorm
    from pgmpy.base import DAG

    return (
        DAG,
        Final,
        Literal,
        alt,
        gaussian_kde,
        json,
        mo,
        np,
        nx,
        pl,
        softmax,
        truncnorm,
        xgb,
    )


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
    # Results
    """)
    return


@app.cell(hide_code=True)
def _(g, json, mo, vars_in_model: list[str]):
    nodes_included_in_model = set(vars_in_model)

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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We are interested in seeing if the model can learn

    $$E[Y|do(E=e), X=x]$$

    The plan:
    1. Simulate a training dataset and train the model
    2. Simulate a test dataset
    3. For each test individual $i$, generate model predictions under counterfactual feature edits:
    $$\hat{Y_i}(E=e) - \hat{Y_i}(E=0)$$
    4. For each individual in the test dataset, simulate the true causal contrast (JOE TODO: many per individual!):
    $$Y_i^{do(E=e)}-Y_i^{do(E=0)}$$
    5. Compare the model contrasts to the true contrasts, individual by individual or averaged over the test population.
    """)
    return


@app.cell
def _(
    EDUCATION_LEVELS: "Final[tuple[str, ...]]",
    mean_edu_incomes_via_simulation,
    mo,
    n_samples,
    n_simulations,
    np,
    pl,
    run_model_simulations,
    simulate_dag,
    vars_in_model: list[str],
    xgb,
):
    mo.stop(not run_model_simulations.value)

    train_data: pl.DataFrame = simulate_dag(
        n=n_samples.value,
        seed=271828,
    )

    model = xgb.XGBRegressor(
        tree_method="hist",
        enable_categorical=True,
    )
    model.fit(
        X=train_data.select(vars_in_model + ["education_level"]),
        y=train_data.select("income"),
    )

    TEST_DATA_SEED = 3141592
    test_data: pl.DataFrame = simulate_dag(
        n=999,
        seed=TEST_DATA_SEED,
    )

    all_preds: list[np.ndarray] = []
    for educ_level in EDUCATION_LEVELS:
        temp_df: pl.DataFrame = test_data.with_columns(
            pl.lit(educ_level)
            .cast(train_data.schema["education_level"])
            .alias("education_level")
        ).select(vars_in_model + ["education_level"])
        preds = model.predict(temp_df)
        all_preds.append(
            pl.Series(
                name=f"pred_do_edu{educ_level}",
                values=preds,
            )
        )
    preds_df: pl.DataFrame = pl.DataFrame(all_preds)


    test_data = (
        test_data.lazy()
        .with_columns(
            pl.struct(
                "ability_motivation",
                "education_institution",
                "family_wealth",
                "location",
                "parents_education",
                "test_scores",
                "scholarship",
            )
            .map_elements(
                lambda row: mean_edu_incomes_via_simulation(
                    n_sims=n_simulations.value, **row
                ),
                return_dtype=pl.Struct(
                    {
                        "income_do_edu0": pl.Float64,
                        "income_do_edu1": pl.Float64,
                        "income_do_edu2": pl.Float64,
                        "income_do_edu3": pl.Float64,
                        "income_do_edu4": pl.Float64,
                        "income_do_edu5": pl.Float64,
                    }
                ),
            )
            .alias("sim")
        )
        .unnest("sim")
        .collect()
    )
    return (preds_df,)


@app.cell(hide_code=True)
def _(preds_df: "pl.DataFrame"):
    preds_df
    return


@app.cell(column=2, hide_code=True)
def _(mo):
    mo.md(r"""
    # The Difference between Conditioning and Intervening
    """)
    return


@app.cell
def _(EDUCATION_LEVELS: "Final[tuple[str, ...]]", pl, simulate_dag):
    population_size: int = 9_999
    seed = 3415192
    observed_population: pl.DataFrame = simulate_dag(n=population_size, seed=seed)
    interven_populations: dict[str, pl.DataFrame] = {}
    for edu_level in EDUCATION_LEVELS:
        interven_populations[edu_level] = simulate_dag(
            n=population_size,
            education_level=edu_level,
            seed=seed,
        )
    return interven_populations, observed_population


@app.cell(hide_code=True)
def _(
    EDUCATION_LEVELS: "Final[tuple[str, ...]]",
    alt,
    gaussian_kde,
    interven_populations: "dict[str, pl.DataFrame]",
    np,
    observed_population: "pl.DataFrame",
    pl,
):
    # ------------------------------------------------------------
    # Shared x-domain
    # ------------------------------------------------------------

    all_income_arrays = [
        observed_population["income"].to_numpy(),
        *[
            population["income"].to_numpy()
            for population in interven_populations.values()
        ],
    ]

    income_min = min(float(values.min()) for values in all_income_arrays)
    income_max = max(float(values.max()) for values in all_income_arrays)
    income_max = 100_000

    # One common evaluation grid for every density.
    # Because income is highly right-skewed, 400–800 points is usually enough.
    x_grid = np.linspace(income_min, income_max, 600)


    # ------------------------------------------------------------
    # Precompute KDEs
    # ------------------------------------------------------------


    def kde_rows(
        income: np.ndarray,
        education_level: str,
        population_type: str,
    ) -> pl.DataFrame:
        income = income[np.isfinite(income)]

        if len(income) < 2 or np.all(income == income[0]):
            density = np.zeros_like(x_grid)
        else:
            density = gaussian_kde(income)(x_grid)

        return pl.DataFrame(
            {
                "income": x_grid,
                "density": density,
                "education_level": education_level,
                "population_type": population_type,
            }
        )


    observed_density_data = pl.concat(
        [
            kde_rows(
                income=observed_population.filter(
                    pl.col("education_level") == edu_level
                )["income"].to_numpy(),
                education_level=edu_level,
                population_type="Observed",
            )
            for edu_level in EDUCATION_LEVELS
        ]
    )

    interventional_density_data = pl.concat(
        [
            kde_rows(
                income=interven_populations[edu_level]["income"].to_numpy(),
                education_level=edu_level,
                population_type="Interventional",
            )
            for edu_level in EDUCATION_LEVELS
        ]
    )


    # ------------------------------------------------------------
    # Plot
    # ------------------------------------------------------------

    education_domain = list(EDUCATION_LEVELS)

    education_range = [
        "#4C78A8",
        "#F58518",
        "#E45756",
        "#72B7B2",
        "#54A24B",
        "#B279A2",
    ]


    def density_chart(
        data: pl.DataFrame,
        title: str,
    ) -> alt.Chart:
        return (
            alt.Chart(data)
            .mark_area(
                opacity=0.25,
                line=True,
                interpolate="monotone",
            )
            .encode(
                x=alt.X(
                    "income:Q",
                    title="Monthly income (ZAR)",
                    scale=alt.Scale(
                        domain=[income_min, income_max],
                        nice=False,
                    ),
                    axis=alt.Axis(format=",.0f"),
                ),
                y=alt.Y(
                    "density:Q",
                    title="Density",
                    stack=None,
                ),
                color=alt.Color(
                    "education_level:N",
                    title="Education level",
                    sort=education_domain,
                    scale=alt.Scale(
                        domain=education_domain,
                        range=education_range,
                    ),
                ),
                tooltip=[
                    alt.Tooltip(
                        "education_level:N",
                        title="Education level",
                    ),
                    alt.Tooltip(
                        "income:Q",
                        title="Monthly income",
                        format=",.0f",
                    ),
                    alt.Tooltip(
                        "density:Q",
                        title="Density",
                        format=".6f",
                    ),
                ],
            )
            .properties(
                width=850,
                height=250,
                title=title,
            )
        )


    observed_chart = density_chart(
        observed_density_data,
        "Observed: P(income | education level)",
    )

    interventional_chart = density_chart(
        interventional_density_data,
        "Interventional: P(income | do(education level))",
    )

    dbns_chart = (
        alt.vconcat(
            observed_chart,
            interventional_chart,
            spacing=25,
        )
        .resolve_scale(
            x="shared",
            color="shared",
            y="independent",
        )
        .properties(title="Observed versus interventional income distributions")
    )

    dbns_chart
    return


@app.cell(hide_code=True)
def _(
    EDUCATION_LEVELS: "Final[tuple[str, ...]]",
    alt,
    gaussian_kde,
    interven_populations: "dict[str, pl.DataFrame]",
    np,
    observed_population: "pl.DataFrame",
    pl,
):
    def make_kde_data(
        observed_population: pl.DataFrame,
        intervention_populations: dict[str, pl.DataFrame],
        education_levels: tuple[str, ...],
        *,
        grid_points: int = 500,
        trim_quantiles: tuple[float, float] | None = None,
    ) -> pl.DataFrame:
        """
        Create precomputed KDE data for observed and interventional income.

        Each education level gets its own x-grid and therefore its own
        minimum and maximum x-axis values.

        Set trim_quantiles=(0.001, 0.999), for example, to prevent a few extreme
        income values from dominating each panel's x-axis.
        """
        frames: list[pl.DataFrame] = []

        for edu_level in education_levels:
            observed_income = (
                observed_population.filter(pl.col("education_level") == edu_level)
                .get_column("income")
                .to_numpy()
            )

            interventional_income = (
                intervention_populations[edu_level].get_column("income").to_numpy()
            )

            observed_income = observed_income[np.isfinite(observed_income)]
            interventional_income = interventional_income[
                np.isfinite(interventional_income)
            ]

            combined_income = np.concatenate(
                [observed_income, interventional_income]
            )

            if trim_quantiles is None:
                x_min = float(combined_income.min())
                x_max = float(combined_income.max())
            else:
                lower_q, upper_q = trim_quantiles
                x_min, x_max = np.quantile(
                    combined_income,
                    [lower_q, upper_q],
                )

            if x_min == x_max:
                padding = max(abs(x_min) * 0.01, 1.0)
                x_min -= padding
                x_max += padding

            x_grid = np.linspace(x_min, x_max, grid_points)

            for population_type, income in (
                ("Observed", observed_income),
                ("Interventional", interventional_income),
            ):
                if len(income) < 2 or np.all(income == income[0]):
                    density = np.zeros_like(x_grid)
                else:
                    density = gaussian_kde(income)(x_grid)

                frames.append(
                    pl.DataFrame(
                        {
                            "education_level": edu_level,
                            "population_type": population_type,
                            "income": x_grid,
                            "density": density,
                        }
                    )
                )

        return pl.concat(frames)


    density_data = make_kde_data(
        observed_population=observed_population,
        intervention_populations=interven_populations,
        education_levels=EDUCATION_LEVELS,
        grid_points=500,
        trim_quantiles=(0.00, 0.99),
    )

    education_order = list(EDUCATION_LEVELS)

    charts = (
        alt.Chart(density_data)
        .mark_area(
            opacity=0.28,
            line=True,
            interpolate="monotone",
        )
        .encode(
            x=alt.X(
                "income:Q",
                title="Monthly income (ZAR)",
                axis=alt.Axis(format=",.0f"),
            ),
            y=alt.Y(
                "density:Q",
                title="Density",
                stack=None,
            ),
            color=alt.Color(
                "population_type:N",
                title="Population",
                scale=alt.Scale(
                    domain=["Observed", "Interventional"],
                    range=["#4C78A8", "#F58518"],
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    "education_level:N",
                    title="Education level",
                ),
                alt.Tooltip(
                    "population_type:N",
                    title="Population",
                ),
                alt.Tooltip(
                    "income:Q",
                    title="Monthly income",
                    format=",.0f",
                ),
                alt.Tooltip(
                    "density:Q",
                    title="Density",
                    format=".6f",
                ),
            ],
        )
        .properties(
            width=420,
            height=220,
        )
        .facet(
            facet=alt.Facet(
                "education_level:N",
                title=None,
                sort=education_order,
                header=alt.Header(
                    labelFontSize=13,
                    labelFontWeight="bold",
                    labelLimit=400,
                ),
            ),
            columns=2,
            title=alt.Title(
                "Observed versus interventional income distributions",
                subtitle=(
                    "Each panel compares P(income | education level) with "
                    "P(income | do(education level))"
                ),
            ),
        )
        .resolve_scale(
            x="independent",
            y="independent",
        )
    )

    charts
    return


@app.cell(column=3, hide_code=True)
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

    run_model_simulations = mo.ui.run_button(label="Run model simulations")
    n_samples = mo.ui.number(
        start=1, stop=100_000, value=999, label="Number of samples"
    )
    n_simulations = mo.ui.number(
        start=1, stop=100_000, value=50, label="Number of simulations"
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
            n_samples,
            n_simulations,
            run_model_simulations,
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
        n_samples,
        n_simulations,
        run_model_simulations,
    )


@app.cell(hide_code=True)
def _(
    include_var__education_institution,
    include_var__family_wealth,
    include_var__location,
    include_var__occupation,
    include_var__parents_education,
    include_var__profess_network,
    include_var__scholarship,
    include_var__survey_participation,
    include_var__test_scores,
):
    vars_in_model: list[str] = []
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
            vars_in_model.append(vbl_name)
    print("variables included in model: ", ", ".join(vars_in_model))
    return (vars_in_model,)


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


@app.cell(column=4, hide_code=True)
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


@app.cell(column=5, hide_code=True)
def _(mo):
    mo.md(r"""
    # Internals
    """)
    return


@app.cell
def _(Final, Literal, np, pl, softmax, truncnorm):
    # from statsmodels.sandbox.distributions.otherdist import loc

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

    PROVINCES: Final[tuple[str, ...]] = (
        "Gauteng",
        "KwaZulu-Natal",
        "Western Cape",
        "Eastern Cape",
        "Limpopo",
        "Mpumalanga",
        "North West",
        "Free State",
        "Northern Cape",
    )

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

    EDUCATION_LEVELS: Final[tuple[str, ...]] = (
        "0-no-formal-education",
        "1-primary",
        "2-secondary",
        "3-tertiary-undergrad",
        "4-tertiary-masters",
        "5-tertiary-phd",
    )

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

    POP_LOG_WEALTH_MEAN: Final[float] = 10.5
    POP_LOG_WEALTH_STD: Final[float] = 1.4
    POP_LOG_INCOME_MEAN: Final[float] = 10
    POP_LOG_INCOME_STD: Final[float] = 2.15

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
        seed: int | None = None,
        education_level: str | None = None,
        ability_motivation: float | None = None,
        education_institution: Literal[*INSTITUTION_LEVELS] | None = None,
        family_wealth: float | None = None,
        location: Literal[*PROVINCES] | None = None,
        parents_education: Literal[*EDUCATION_LEVELS] | None = None,
        test_scores: float | None = None,
        scholarship: bool | None = None,
    ) -> pl.DataFrame:
        """
        Simulate n observations from the education-income causal DAG via
        ancestral sampling.

        Even if there are fixed interventions on variables (e.g. education_level), I
        am still always doing the random draws, which keeps the random-number-stream
        comparable between intervention and non-intervention simulations with the
        same seed.

        Parameters
        ----------
        n : int
            Number of samples to generate.
        seed : int | None
            Random seed for reproducibility.
        education_level : str or None
            Causal intervention do(education_level=e). Must be one of
            EDUCATION_LEVELS. When set, education_level is fixed for all
            observations rather than sampled from its observational distribution
        TODO: finish documenting these params

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
        if ability_motivation is not None:
            ability = np.full(n, ability_motivation, dtype=float)

        # ------------------------------------------------------------------
        # 2. location  ~  Categorical(province_weights)
        # ------------------------------------------------------------------
        location_idx = rng.choice(len(PROVINCES), size=n, p=PROVINCE_WEIGHTS)
        if location is not None:
            location_idx = np.full(n, PROVINCES.index(location), dtype=int)
        is_rural = PROVINCE_IS_RURAL[location_idx]
        wage_scalar = PROVINCE_WAGE_SCALAR[location_idx]

        # ------------------------------------------------------------------
        # 3. parents_education  ~  Categorical(SA marginals)
        # ------------------------------------------------------------------
        parents_edu_idx = rng.choice(
            len(EDUCATION_LEVELS), size=n, p=PARENTS_EDU_PROBS
        )
        if parents_education is not None:
            parents_edu_idx = np.full(
                n, EDUCATION_LEVELS.index(parents_education), dtype=int
            )

        # ------------------------------------------------------------------
        # 4. family_wealth  ~  LogNormal(mu[parents_edu], sigma[parents_edu])
        # ------------------------------------------------------------------

        wealth_mu_vec = WEALTH_MU[parents_edu_idx]
        wealth_sigma_vec = WEALTH_SIGMA[parents_edu_idx]
        family_wealth = rng.lognormal(mean=wealth_mu_vec, sigma=wealth_sigma_vec)
        if family_wealth is not None:
            family_wealth = np.full(n, family_wealth, dtype=float)
        log_wealth = np.log(family_wealth)
        log_wealth_scaled = (log_wealth - POP_LOG_WEALTH_MEAN) / (
            POP_LOG_WEALTH_STD + 1e-8
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
        if test_scores is not None:
            test_scores = np.full(n, test_scores, dtype=float)

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
        if scholarship is not None:
            scholarship = np.full(n, scholarship, dtype=bool)

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
        if education_institution is not None:
            inst_idx = np.full(
                n, INSTITUTION_LEVELS.index(education_institution), dtype=int
            )

        # ------------------------------------------------------------------
        # 8. education_level  ~  Categorical(softmax(logits))  OR  do()
        # ------------------------------------------------------------------
        inst_f = inst_idx.astype(float)
        is_univ_or_elite = (inst_idx >= 2).astype(float)
        is_elite = (inst_idx == 3).astype(float)
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
        if education_level is not None:
            edu_idx = np.full(
                n, EDUCATION_LEVELS.index(education_level), dtype=int
            )

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
        income = rng.lognormal(mean=income_log_mu, sigma=0.5)

        # ------------------------------------------------------------------
        # 12. survey_participation  ~  Bernoulli(sigmoid(logit))
        # ------------------------------------------------------------------
        log_income = np.log(income)
        log_income_scaled = (log_income - POP_LOG_INCOME_MEAN) / (
            POP_LOG_INCOME_STD + 1e-8
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


    def mean_edu_incomes_via_simulation(
        n_sims: int,
        **kwargs,
    ) -> float:
        results: dict = {}
        for i, edu_level in enumerate(EDUCATION_LEVELS):
            sim_results: pl.DataFrame = simulate_dag(
                n=n_sims,
                education_level=edu_level,
                **kwargs,
            )
            results[f"income_do_edu{i}"] = (
                sim_results.select(pl.col("income")).mean().item()
            )
        return results

    return EDUCATION_LEVELS, mean_edu_incomes_via_simulation, simulate_dag


if __name__ == "__main__":
    app.run()
