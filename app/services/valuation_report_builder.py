# app/services/valuation_report_builder.py

from datetime import datetime


def build_report_context(ai_json, user_input, valuation_id=None):    
    built_up_area = (
        user_input.get("built_up_area_sqft")
        or ai_json["property_details"].get("built_up_area_sqft")
    )
    
    year_built = user_input.get("year_built")

    if year_built:
        try:
            construction_year = int(year_built)
            property_age = datetime.now().year - construction_year
        except ValueError:
            construction_year = None
            property_age = None
    else:
        construction_year = None
        property_age = None
    
    report_metadata = {
        "valuation_id": valuation_id or "N/A",
        "date_of_report": datetime.now().strftime("%d %B %Y"),
        "client_name": user_input.get("client_name", "N/A"),
    }

    property_details = {
        "name_of_owner": user_input.get("full_name", "N/A"),
        "project_name": user_input.get("project_name", "N/A"),
        "property_address": ai_json["property_details"].get("address", "N/A"),
        "property_type": ai_json["property_details"].get("property_type", "N/A"),
        "configuration": (
            user_input.get("configuration")
            or ai_json["property_details"].get("configuration")
            or "N/A"
        ),
        "land_area_sqft": ai_json["property_details"].get("land_area_sqft", "N/A"),
        "built_up_area_sqft": built_up_area if built_up_area else "N/A",
        
        "construction_status": (
            user_input.get("construction_status")
            or ai_json["property_details"].get("construction_status")
            or "N/A"
        ),
        "construction_year": (
            construction_year
            or ai_json["property_details"].get("construction_year")
            or "N/A"
        ),
        "property_age_years": (
            property_age
            or ai_json["property_details"].get("age_years")
            or "N/A"
        ),
        "last_sale_date": (
            user_input.get("last_sale_date")
            or ai_json["property_details"].get("last_sale_date")
            or "N/A"
        ),
        "last_sale_price": (
            user_input.get("last_sale_price")
            or ai_json["property_details"].get("last_sale_price")
            or "N/A"
        ),
        "ownership_type": (
            user_input.get("ownership_type")
            or ai_json["property_details"].get("ownership_type")
            or "N/A"
        ),
        "title_details": ai_json["property_details"].get("title_details", "N/A"),
        "purpose_of_report": user_input.get("purpose_of_valuation", "N/A"),
        "type_of_valuation": "Desktop Valuation Opinion",
        "inspection": "No Physical Inspection Conducted",
        "confidentiality": "Strictly for internal reference",
    }
    
    location_identification = {
        "micro_location": (
            user_input.get("micro_location")
            or ai_json["property_details"].get("micro_location")
            or "N/A"
        ),
        "municipal_authority": (
            user_input.get("municipal_authority")
            or ai_json["property_details"].get("municipal_authority")
            or "N/A"
        ),
        "connectivity": (
            user_input.get("connectivity")
            or ai_json["property_details"].get("connectivity")
            or "N/A"
        ),
        "social_infrastructure": (
            user_input.get("social_infrastructure")
            or ai_json["property_details"].get("social_infrastructure")
            or "N/A"
        ),
        "surroundings": (
            user_input.get("surroundings")
            or ai_json["property_details"].get("surroundings")
            or "N/A"
        ),
        "zoning": ai_json["property_details"].get("zoning", "N/A"),
        "demand_profile": (
            user_input.get("demand_profile")
            or ai_json["property_details"].get("demand_profile")
            or "N/A"
        ),
    }

    project_profile = {
        "developer": (
            user_input.get("developer")
            or ai_json["property_details"].get("developer")
            or "N/A"
        ),
        "project_positioning": (
            user_input.get("project_positioning")
            or ai_json["property_details"].get("project_positioning")
            or "N/A"
        ),
        "towers": (
            user_input.get("towers")
            or ai_json["property_details"].get("towers")
            or "N/A"
        ),
        "amenities": (
            user_input.get("amenities")
            or ai_json["property_details"].get("amenities")
            or "N/A"
        ),
        "market_perception": (
            user_input.get("market_perception")
            or ai_json["property_details"].get("market_perception")
            or "N/A"
        ),
    }

    area_details = {
        "carpet_area_sqft": built_up_area if built_up_area else "N/A",
        "layout": (
            user_input.get("layout")
            or ai_json["property_details"].get("layout")
            or "N/A"
        ),
        "floor_plan": (
            user_input.get("floor_plan")
            or ai_json["property_details"].get("floor_plan")
            or "N/A"
        ),
        "current_usage": (
            user_input.get("current_usage")
            or ai_json["property_details"].get("current_usage")
            or "N/A"
        ),
    }


    raw_comparables = ai_json.get("comparables_used", [])

    market_benchmark = []

    for comp in raw_comparables:
        market_benchmark.append({
            "address": comp.get("address", "N/A"),
            "beds_baths": comp.get("beds_baths", "N/A"),
            "land_size_sqft": comp.get("land_size_sqft", "N/A"),
            "sale_date": comp.get("sale_date", "N/A"),
            "sale_price": comp.get("sale_price", "N/A"),
            "distance_km": comp.get("distance_km", "N/A"),
            "comparison_level": comp.get("comparison_level", "Comparable"),
        })
        
    mid_value = ai_json["predicted_value"]["mid_value"]
    area_for_valuation = built_up_area or 0

    adopted_rate = (
        int(mid_value / area_for_valuation)
        if area_for_valuation and area_for_valuation > 0
        else "N/A"
    )

    indicative_market_value = {
        "area_considered_sqft": area_for_valuation,
        "adopted_market_rate": adopted_rate,
        "indicative_value": mid_value,
    }
    
    value_range = {
        "conservative": {
            "value": ai_json["predicted_value"]["low_value"],
            "explanation": ai_json["predicted_value"].get(
                "low_explanation",
                "Lower bound estimate based on conservative assumptions."
            )
        },
        "mid_range": {
            "value": ai_json["predicted_value"]["mid_value"],
            "explanation": ai_json["predicted_value"].get(
                "mid_explanation",
                "Fair market value under normal conditions."
            )
        },
        "optimistic": {
            "value": ai_json["predicted_value"]["high_value"],
            "explanation": ai_json["predicted_value"].get(
                "high_explanation",
                "Upper bound estimate assuming strong demand."
            )
        }
    }
        
    advanced_analytics = {
        "confidence_score": ai_json["predicted_value"].get("confidence_score", 0),
        "recommended_ltv": ai_json.get("bank_lending_model", {}).get("recommended_ltv", 0),
        "safe_lending_value": ai_json.get("bank_lending_model", {}).get("safe_lending_value", 0),
        "risk_level": ai_json.get("bank_lending_model", {}).get("risk_level", "N/A"),
        "valuation_validity_days": ai_json.get("valuation_validity_days", 60),
    }

    nearby_market_evidence = [
        "Recent transactions in nearby premium projects support the adopted rate",
        "Strong demand for ready-to-move residential units",
        "Limited supply of new premium projects in the locality",
        "Healthy resale and rental absorption observed",
    ]

    forecast = ai_json.get("forecast", {})
    current_value = ai_json["predicted_value"]["mid_value"]
    current_year = datetime.now().year

    future_outlook = []
    growth_rates = [
        forecast.get("year_1_growth_percent", 0),
        forecast.get("year_2_growth_percent", 0),
        forecast.get("year_3_growth_percent", 0),
        forecast.get("year_4_growth_percent", 0),
        forecast.get("year_5_growth_percent", 0),
    ]

    base_value = ai_json["predicted_value"]["mid_value"]

    for i, rate in enumerate(growth_rates, start=1):
        projected_value = int(base_value * ((1 + rate / 100) ** i))
        future_outlook.append({
            "year": current_year + i,
            "expected_value": projected_value,
            "growth_percent": rate,
        })
        
    swot_analysis = ai_json.get(
        "swot_analysis",
        {
            "strengths": [],
            "weaknesses": [],
            "opportunities": [],
            "threats": [],
        }
    )
    
    rental_raw = ai_json.get("rental_analysis", {})

    rental_analysis = {
        "estimated_monthly_rent": rental_raw.get("estimated_monthly_rent", 0),
        "estimated_annual_rent": rental_raw.get("estimated_annual_rent", 0),
        "rental_yield_percent": rental_raw.get("rental_yield_percent", 0),
        "rental_demand_level": rental_raw.get("rental_demand_level", "N/A"),
        "average_rent_locality": rental_raw.get("average_rent_locality", 0),
        "nearby_rental_comparables": rental_raw.get("nearby_rental_comparables", []),
    }
    
    disclaimer = [
        "This report is a Desktop Valuation Opinion prepared using secondary market data.",
        "No physical or on-site inspection of the subject property has been carried out.",
        "The value stated represents an indicative market value for cross-check/reference purposes only.",
        "Actual realizable value may vary based on physical condition, legal status, negotiations, and market sentiment.",
        "This report is not intended for statutory, legal, lending, or enforcement purposes.",
        "No responsibility is assumed for title verification, encumbrances, or statutory approvals.",
        "This report is confidential and intended solely for the client.",
    ]

    return {
        "property_details": property_details,
        "report_metadata": report_metadata,
        "location_identification": location_identification,
        "project_profile": project_profile,
        "area_details": area_details,
        "market_benchmark": market_benchmark,
        "indicative_market_value": indicative_market_value,
        "value_range": value_range,
        "advanced_analytics": advanced_analytics,
        "nearby_market_evidence": nearby_market_evidence,
        "future_outlook": future_outlook,
        "swot_analysis": swot_analysis,
        "rental_analysis": rental_analysis,
        "disclaimer": disclaimer,
    }
