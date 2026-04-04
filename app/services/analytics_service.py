import json
from sqlalchemy.orm import Session
from app.db.database import redis_client
from app.db.repositories.records_repo import RecordsRepository


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
        self.records_repository = RecordsRepository(db=self.db)

    def get_dashboard_summary(self,user_id:int):
        cache_key = f"dashboard:summary:{user_id}"

        cached_data = redis_client.get(cache_key)

        if cached_data:
            return json.loads(cached_data)
        
        records = self.records_repository.get_records()

        total_records = len(records)
        total_amount = sum(record.amount for record in records)
        total_income = sum(record.amount for record in records if record.transaction_type == "income")
        total_expense = sum(record.amount for record in records if record.transaction_type == "expense")
        net_balance = total_income - total_expense
        savings_rate = round((net_balance / total_income * 100), 2) if total_income > 0 else 0
        avg_transaction = round(total_amount / total_records, 2) if total_records > 0 else 0
        
        category_breakdown = {}
        for r in records:
            category_breakdown[r.category] = category_breakdown.get(r.category, 0) + r.amount

        summary = {
            "total_records": total_records,
            "total_income": total_income,
            "total_expense": total_expense,
            "net_balance": net_balance,
            "savings_rate": f"{savings_rate}%",
            "avg_transaction_value": avg_transaction,
            "category_breakdown": category_breakdown,
            "highest_single_expense": max([r.amount for r in records if r.transaction_type == "expense"], default=0)
        }

        redis_client.setex(cache_key, 300, json.dumps(summary)) 

        return summary

