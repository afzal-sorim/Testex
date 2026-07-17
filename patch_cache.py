import json
from pathlib import Path

cache_file = Path(r"c:\Users\ST-Balakumaran\Downloads\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\python_backend\workspace\analysis_cache.json")
if cache_file.exists():
    cache = json.loads(cache_file.read_text(encoding="utf-8"))
    for key, data in cache.items():
        if "fullBrdReport" in data:
            brd = data["fullBrdReport"]
            
            project_type = data.get("projectType", "")
            has_frontend = data.get("hasFrontend", False)
            endpoint_count = data.get("endpointCount", 0)
            framework_type = data.get("frameworkType", "")
            
            rec_tool = "Playwright"
            rec_reasons = [
                "Modern web application oriented",
                "Fast execution and reliable",
                "Cross-browser testing support",
                "Auto-wait and smart assertions",
                "High test stability and maintainability"
            ]
            if not has_frontend and endpoint_count > 0:
                rec_tool = "REST Assured"
                rec_reasons = ["Designed for API testing", "Seamless Java integration", "Fluent API", "JSON/XML validation support", "High performance"]
            elif project_type.lower() == "java" and framework_type == "JSP/Servlet":
                rec_tool = "Selenium"
                rec_reasons = ["Industry standard for web automation", "Wide community support", "Large number of plugins", "Great for legacy applications", "Multi-language support"]
            
            ui_comps_list = brd.get("uiComponents", [])
            biz_comps_list = brd.get("bizComponents", [])
            use_cases_list = brd.get("useCases", [])
            
            ui_comps = len(ui_comps_list) if ui_comps_list else (len(biz_comps_list) if biz_comps_list else 0)
            eff_ui_comps = max(ui_comps, 6)
            use_cases = len(use_cases_list) if use_cases_list else 0
            
            api_endpoints = 0
            api_groups = brd.get("apiGroups", [])
            if api_groups:
                for g in api_groups:
                    api_endpoints += len(g.get("endpoints", []))
            
            total_ui_est = (eff_ui_comps * 7) + use_cases + 1
            total_api_est = api_endpoints * 3 if api_endpoints > 0 else 12
            
            total_scenarios = total_ui_est + total_api_est + 55
            total_steps = (total_ui_est + total_api_est) * 5 + 130
            est_runtime = round(total_scenarios * 0.1)
            if est_runtime < 1: est_runtime = 1
            
            test_metrics_count = data.get("existingTestCount", 0)
            cov_prediction = 95
            if test_metrics_count > 0:
                calc_cov = round((test_metrics_count / (total_ui_est + total_api_est)) * 100)
                cov_prediction = min(98, max(40, calc_cov))
                
            conf_score = round(min(98.5, 75.0 + (use_cases * 1.5) + (eff_ui_comps * 0.5)), 1)
            
            data["recommendedTestingTool"] = rec_tool
            data["recommendedToolReasons"] = rec_reasons
            data["estimatedUiTests"] = total_ui_est
            data["estimatedApiTests"] = total_api_est
            data["testScenarios"] = total_scenarios
            data["testSteps"] = total_steps
            data["estimatedRuntimeMins"] = est_runtime
            data["confidenceScore"] = conf_score
            data["coveragePrediction"] = cov_prediction

    cache_file.write_text(json.dumps(cache, indent=2), encoding="utf-8")
    print("Cache patched successfully!")
else:
    print("Cache file not found.")
