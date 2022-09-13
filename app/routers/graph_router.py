from fastapi import APIRouter

from app.data import MongoDB
from app.graphs import stacked_bar_chart, df_tech_stack_by_role

Router = APIRouter(
    tags=["Graph Operations"],
)
Router.db = MongoDB()


@Router.get("/graph/tech-stack-by-role")
async def tech_stack_by_role():
    """Tech Stack Count by Role, stacked bar chart
    <pre><code>
    @return JSON[Altair.Chart]</pre></code>"""
    return stacked_bar_chart(
        df_tech_stack_by_role(Router.db),
        "tech_stack",
        "role",
    ).to_dict()
