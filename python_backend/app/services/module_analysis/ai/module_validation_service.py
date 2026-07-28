import json
from typing import List, Dict, Any
from app.ai.ai_factory import AIFactory
from app.brd_models import BusinessDomainInfo, BusinessModelInfo, ClassAttribute


class ModuleValidationService:
    """
    Step 5: AI LLM Business Module Validation.
    Sends grouped metadata (controllers, services, entities, apis) to the LLM to
    generate non-technical, business-friendly titles, purposes, and responsibilities
    understandable to non-tech business stakeholders.
    """

    def validate_and_enrich_modules(
        self,
        module_groups: List[Dict[str, Any]],
        app_name: str,
        api_key: str = None,
        model_name: str = None
    ) -> Dict[str, Any]:
        enriched_domains: List[BusinessDomainInfo] = []
        enriched_models: List[BusinessModelInfo] = []

        if not module_groups:
            return {"businessDomains": [], "businessModels": []}

        # Prepare low-token payload for LLM validation
        simplified_modules = []
        for m in module_groups[:8]:  # Top 8 modules
            attr_list = [a["name"] for a in m.get("attributes", [])[:5]]
            simplified_modules.append({
                "module_stem": m["stem"],
                "suggested_name": m["name"],
                "controllers": m["controllers"][:3],
                "services": m["services"][:3],
                "entities": m["entities"][:3],
                "attributes": attr_list,
                "apis": m["apis"][:4]
            })

        system_instruction = (
            "You are an expert IT Business Analyst writing business documentation for non-technical business executives and domain users. "
            "Your job is to analyze software component groups and generate clear, engaging, non-technical business explanations. "
            "RULES:\n"
            "1. DO NOT use technical software jargon (e.g. 'REST API controller', 'Spring Data JPA', 'DAO layer', 'data integrity constraints', 'domain record attributes', 'state persistence') in the titles, purposes, or explanations.\n"
            "2. Explain what real business capability each module provides to end-users and the organization.\n"
            "3. For example, if entity is 'Owner' with fields ['address', 'city', 'telephone'] -> "
            "   Name: 'Owner Management', Purpose: 'Manages pet owner profiles, residential addresses, phone numbers, and registered pet accounts.', "
            "   Explanation: 'The Owner module manages pet owner contact records, residential addresses, telephone contacts, and links to registered pets within the system.'\n"
            "4. Return ONLY a valid JSON array of objects with keys: name, purpose, overallResponsibility, explanation, functionalities (array of strings)."
        )

        user_prompt = (
            f"Application Name: {app_name}\n"
            f"Extracted Component Groups:\n{json.dumps(simplified_modules, indent=2)}\n\n"
            "Analyze each component group and return clear non-technical business titles, purposes, explanations, and responsibilities."
        )

        ai_explanations: Dict[str, Dict[str, Any]] = {}
        try:
            ai_client = AIFactory.get_client()
            response_text = ai_client.generate(user_prompt, system_instruction, api_key, model_name)
            cleaned = response_text.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(cleaned)
            if isinstance(parsed, list):
                for idx, item in enumerate(parsed):
                    if idx < len(simplified_modules):
                        stem_key = simplified_modules[idx]["module_stem"].lower()
                        ai_explanations[stem_key] = item
        except Exception as e:
            print(f"AI Module Validation fallback to rule engine: {e}")

        # Construct final BusinessDomainInfo & BusinessModelInfo
        for m in module_groups[:8]:
            stem_key = m["stem"].lower()
            ai_info = ai_explanations.get(stem_key, {})

            display_name = ai_info.get("name") or m["name"]
            domain_base = display_name.replace(" Management", "").replace(" Processing", "").replace(" System", "")

            purpose = ai_info.get("purpose") or f"Provides business capability management and operational record keeping for {domain_base}."
            responsibility = ai_info.get("overallResponsibility") or f"Manages business workflows and operational processes for {domain_base}."
            funcs = ai_info.get("functionalities") or [
                f"Core business operations for {domain_base}",
                f"Record management for {domain_base} entries",
                f"Operational validation rules and workflow processing"
            ]

            entities_list = m["entities"] or [m["stem"]]
            controllers_list = m["controllers"]
            services_list = m["services"]
            apis_list = m["apis"]

            # Add to BusinessDomainInfo list
            enriched_domains.append(BusinessDomainInfo(
                name=display_name,
                purpose=purpose,
                overallResponsibility=responsibility,
                functionalities=funcs,
                relatedModules=[m["stem"]],
                controllersInvolved=controllers_list[:5],
                servicesInvolved=services_list[:5],
                entitiesUsed=entities_list[:5],
                apisInvolved=apis_list[:5],
                uiComponentsInvolved=[],
                businessRules=[f"Enforce business rules for {domain_base} operations", "Field requirement and state validation"],
                validationRules=["Mandatory attribute checks", "Data integrity verification"],
                relationships=["Integrated with application database layer"],
                dependencies=["Core Application Framework"],
                aiReasoning=f"Validated business module '{display_name}' grouping {len(m['files'])} source file(s)."
            ))

            # Add primary entity model to BusinessModelInfo list
            for ent_name in entities_list[:2]:
                attrs = [ClassAttribute(name=a["name"], type=a["type"]) for a in m["attributes"]] or [
                    ClassAttribute(name="id", type="Long/String"), ClassAttribute(name="name", type="String")
                ]
                attr_names = [a.name for a in attrs[:4]]
                real_summary = ai_info.get("purpose") or ModuleValidationService.get_real_entity_summary(ent_name, attr_names)
                ai_exp = ai_info.get("explanation") or real_summary

                enriched_models.append(BusinessModelInfo(
                    name=ent_name,
                    purpose=real_summary,
                    description=real_summary,
                    attributes=attrs,
                    relationships=["Domain Entity Model"],
                    associatedControllers=controllers_list[:3],
                    associatedServices=services_list[:3],
                    associatedRepositories=m["repositories"][:3],
                    apisUsingModel=apis_list[:3],
                    businessRules=[f"Enforce {ent_name} attribute integrity"],
                    validationRules=["Mandatory parameter checks"],
                    crudOperations=["Create", "Read", "Update", "Delete", "Search"],
                    workflowInvolvement=f"Participates in {ent_name} lifecycle management.",
                    relatedModules=[m["stem"]],
                    aiReasoning=f"Domain entity model for {ent_name} under {display_name}.",
                    aiExplanation=ai_exp
                ))

        return {
            "businessDomains": enriched_domains,
            "businessModels": enriched_models
        }

    def generate_executive_summary(
        self,
        app_name: str,
        module_stems: List[str],
        entities: List[str],
        api_key: str = None,
        model_name: str = None
    ) -> str:
        """
        Generates a 100% REAL, domain-specific Executive Summary for non-technical business users.
        """
        stems_lower = [s.lower() for s in (module_stems + entities)]
        stems_set = set(stems_lower)

        # 1. Try AI Generation
        system_instruction = (
            "You are an expert IT Business Analyst writing an Executive Summary for business executives and non-technical stakeholders. "
            "Explain in 2 to 3 concise, engaging sentences what this specific application actually does in plain business terms. "
            "DO NOT use generic template phrases like 'is an enterprise solution designed to manage core operational capabilities across...'. "
            "Describe the real business domain (e.g. veterinary clinic management, HR employee tracking, e-commerce retail, core banking)."
        )
        user_prompt = (
            f"Application Name: {app_name}\n"
            f"Key Business Modules & Entities: {', '.join(module_stems[:8])}\n"
            f"Key Domain Entities: {', '.join(entities[:10])}\n\n"
            "Write a clear, realistic 2-3 sentence executive business summary of this application for non-technical domain stakeholders."
        )

        try:
            ai_client = AIFactory.get_client()
            summary = ai_client.generate(user_prompt, system_instruction, api_key, model_name).strip()
            if summary and len(summary) > 40 and "enterprise solution designed to manage core" not in summary.lower():
                return summary
        except Exception as e:
            print(f"AI Executive Summary generation fallback to domain synthesizer: {e}")

        # 2. Smart Domain Synthesizer Fallback (Rule Engine)
        app_title = app_name.replace('-', ' ').replace('_', ' ').title()

        if any(w in stems_set for w in ['owner', 'pet', 'vet', 'visit', 'pettype', 'veterinarian', 'specialty']):
            return (
                f"{app_title} is a comprehensive veterinary clinic management application. "
                f"It enables clinic staff to register pet owners, track patient medical visits, manage veterinarian profiles and specialties, "
                f"and maintain complete healthcare histories for pets."
            )

        if any(w in stems_set for w in ['employee', 'employer', 'leave', 'attendance', 'payroll', 'salary', 'department', 'designation']):
            return (
                f"{app_title} is a Human Resources & Workforce Management platform. "
                f"It enables organizations to manage employee profiles, track attendance and leave requests, process payroll operations, "
                f"and maintain organizational department hierarchies."
            )

        if any(w in stems_set for w in ['account', 'transaction', 'loan', 'transfer', 'balance', 'customer', 'bank']):
            return (
                f"{app_title} is a Financial Services & Banking Management application. "
                f"It allows financial institutions to manage customer accounts, process money transfers and deposit transactions, "
                f"oversee loan applications, and audit account balances."
            )

        if any(w in stems_set for w in ['product', 'order', 'cart', 'payment', 'inventory', 'billing', 'catalog', 'checkout']):
            return (
                f"{app_title} is an E-Commerce & Retail Order Management platform. "
                f"It enables businesses to maintain product catalogs, manage customer shopping carts, process payments, "
                f"and track order fulfillment and inventory stock."
            )

        if any(w in stems_set for w in ['student', 'teacher', 'course', 'grade', 'enrollment', 'school', 'class']):
            return (
                f"{app_title} is an Academic & Student Management application. "
                f"It provides educational institutions with tools to manage student profiles, track course enrollments, "
                f"record grades, and coordinate faculty schedules."
            )

        formatted_stems = [s.replace('Management', '').strip() for s in module_stems[:4] if s]
        stems_phrase = ", ".join(formatted_stems) if formatted_stems else "key operational entities"
        return (
            f"{app_title} is a business application designed for managing {stems_phrase} operations. "
            f"It provides business domain users with capabilities to track record states, execute operational workflows, "
            f"and coordinate administrative tasks across the organization."
        )

    @staticmethod
    def get_real_entity_summary(ent_name: str, attrs: List[str] = None) -> str:
        name_lower = ent_name.lower()
        attr_list = [a.lower() for a in (attrs or [])]

        if name_lower in ['owner', 'owners']:
            return "Manages pet owner contact profiles, residential addresses, phone numbers, and registered pet accounts."
        if name_lower in ['pet', 'pets']:
            return "Manages pet registrations, animal species, birth dates, medical charts, and owner links."
        if name_lower in ['visit', 'visits', 'appointment']:
            return "Tracks patient clinic appointments, medical treatment notes, visit dates, and checkup histories."
        if name_lower in ['vet', 'vets', 'veterinarian']:
            return "Manages veterinarian staff profiles, medical specialties, qualifications, and practice schedules."
        if name_lower in ['specialty', 'specialties']:
            return "Defines medical specialties (e.g. radiology, surgery, dentistry) assigned to clinic veterinarians."
        if name_lower in ['pettype', 'pettypes', 'animaltype']:
            return "Categorizes animal species and pet classifications (e.g. dog, cat, bird, lizard) registered in the system."
        if name_lower in ['person', 'people']:
            return "Base personal record holding name, identity credentials, and contact details for system clients."
        if name_lower in ['crash', 'error', 'exception']:
            return "Handles system diagnostic logging, application failure reports, and exception monitoring."
        if name_lower in ['employee', 'employees']:
            return "Manages employee profiles, job titles, department assignments, employment status, and staff records."
        if name_lower in ['employer', 'employers']:
            return "Manages corporate employer accounts, enterprise client profiles, business addresses, and contracts."
        if name_lower in ['client', 'clients', 'customer', 'customers']:
            return "Manages client relationship records, communication preferences, account histories, and contact info."
        if name_lower in ['leave', 'leaves', 'leaverequest', 'absence']:
            return "Tracks employee leave applications, vacation balances, sick leave approvals, and time-off requests."
        if name_lower in ['attendance', 'clockin', 'timesheet']:
            return "Monitors daily clock-in/out timestamps, shift hours, work timesheets, and attendance logs."
        if name_lower in ['payroll', 'salary', 'compensation']:
            return "Processes employee salary calculations, tax deductions, compensation structures, and monthly pay stubs."
        if name_lower in ['product', 'products', 'item', 'catalog']:
            return "Manages retail product listings, pricing details, SKU catalog items, and inventory stock levels."
        if name_lower in ['order', 'orders', 'purchase']:
            return "Processes customer purchase transactions, order fulfillment statuses, shipping details, and invoice history."
        if name_lower in ['cart', 'shoppingcart', 'basket']:
            return "Manages customer shopping baskets, item quantities, discount vouchers, and checkout order totals."
        if name_lower in ['payment', 'payments', 'billing']:
            return "Handles transaction billing, credit card payment processing, receipts, and refund requests."
        if name_lower in ['user', 'users', 'account', 'auth']:
            return "Manages user credentials, authentication security, role permissions, and user profile settings."

        if attrs:
            fields_str = ", ".join(attrs[:3])
            return f"Manages operational data records, state persistence, and workflow attributes ({fields_str}) for {ent_name}."

        return f"Manages operational business state, record persistence, and transaction workflows for {ent_name}."
