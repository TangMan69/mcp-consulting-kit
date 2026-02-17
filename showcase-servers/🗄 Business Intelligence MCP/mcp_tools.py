from pydantic import BaseModel
from typing import Optional
from db import run_query
from llm_provider import get_llm_provider

class NLQueryRequest(BaseModel):
    query: str
    schema_hint: Optional[str] = None

def handle_nl_query(payload: NLQueryRequest):
    llm = get_llm_provider()
    sql = llm.generate_sql(payload.query, payload.schema_hint)
    rows = run_query(sql)
    return {"sql": sql, "rows": rows}
