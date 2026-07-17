import sys
import re

models_path = r"c:\Users\ST-Balakumaran\Downloads\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\python_backend\app\models.py"

with open(models_path, "r", encoding="utf-8") as f:
    models_content = f.read()

new_fields = """    existingTestTypes: Optional[str] = "Not Detected"
    recommendedTestingTool: Optional[str] = "Playwright"
    recommendedToolReasons: List[str] = []
    coveragePrediction: int = 0
    estimatedUiTests: int = 0
    estimatedApiTests: int = 0
    testScenarios: int = 0
    testSteps: int = 0
    estimatedRuntimeMins: int = 0
    confidenceScore: float = 0.0"""

models_content = models_content.replace('    existingTestTypes: Optional[str] = "Not Detected"', new_fields)

with open(models_path, "w", encoding="utf-8") as f:
    f.write(models_content)


analysis_path = r"c:\Users\ST-Balakumaran\Downloads\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\python_backend\app\services\analysis_service.py"
with open(analysis_path, "r", encoding="utf-8") as f:
    analysis_content = f.read()

calc_logic = """            test_metrics = self.scan_existing_tests(clone_dir, is_java)
            
            # Dynamic metrics generation
            rec_tool = "Playwright"
            rec_reasons = [
                "Modern web application oriented",
                "Fast execution and reliable",
                "Cross-browser testing support",
                "Auto-wait and smart assertions",
                "High test stability and maintainability"
            ]
            if not project_info.get("has_frontend") and project_info.get("endpoint_count", 0) > 0:
                rec_tool = "REST Assured"
                rec_reasons = ["Designed for API testing", "Seamless Java integration", "Fluent API", "JSON/XML validation support", "High performance"]
            elif project_type.lower() == "java" and project_info.get("framework_type") == "JSP/Servlet":
                rec_tool = "Selenium"
                rec_reasons = ["Industry standard for web automation", "Wide community support", "Large number of plugins", "Great for legacy applications", "Multi-language support"]
                
            ui_comps = len(brd_summary.uiComponents) if getattr(brd_summary, 'uiComponents', None) else (len(brd_summary.bizComponents) if getattr(brd_summary, 'bizComponents', None) else 0)
            eff_ui_comps = max(ui_comps, 6)
            use_cases = len(brd_summary.useCases) if getattr(brd_summary, 'useCases', None) else 0
            api_endpoints = sum(len(g.endpoints) if getattr(g, 'endpoints', None) else 0 for g in (getattr(brd_summary, 'apiGroups', None) or []))
            
            total_ui_est = (eff_ui_comps * 7) + use_cases + 1
            total_api_est = api_endpoints * 3 if api_endpoints > 0 else 12
            
            total_scenarios = total_ui_est + total_api_est + 55
            total_steps = (total_ui_est + total_api_est) * 5 + 130
            est_runtime = round(total_scenarios * 0.1)
            if est_runtime < 1: est_runtime = 1
            
            cov_prediction = 95
            if test_metrics.get("count", 0) > 0:
                calc_cov = round((test_metrics.get("count", 0) / (total_ui_est + total_api_est)) * 100)
                cov_prediction = min(98, max(40, calc_cov))
                
            conf_score = round(min(98.5, 75.0 + (use_cases * 1.5) + (eff_ui_comps * 0.5)), 1)
"""

analysis_content = analysis_content.replace("            test_metrics = self.scan_existing_tests(clone_dir, is_java)", calc_logic)

response_fields = """                existingTestFailed=test_metrics.get("failed", 0),
                existingTestTypes=test_metrics.get("types", "Not Detected"),
                recommendedTestingTool=rec_tool,
                recommendedToolReasons=rec_reasons,
                coveragePrediction=cov_prediction,
                estimatedUiTests=total_ui_est,
                estimatedApiTests=total_api_est,
                testScenarios=total_scenarios,
                testSteps=total_steps,
                estimatedRuntimeMins=est_runtime,
                confidenceScore=conf_score,
                errorMessage=None,"""

analysis_content = analysis_content.replace("""                existingTestFailed=test_metrics.get("failed", 0),
                existingTestTypes=test_metrics.get("types", "Not Detected"),
                errorMessage=None,""", response_fields)

with open(analysis_path, "w", encoding="utf-8") as f:
    f.write(analysis_content)


front_path = r"c:\Users\ST-Balakumaran\Downloads\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\frontend\src\pages\AITestRecommendation.jsx"
with open(front_path, "r", encoding="utf-8") as f:
    front_content = f.read()

import re
front_content = re.sub(r"const calculateTestStats = \(\) => \{.*?\};\n\n  const \{ totalUi, totalApi, testScenarios, testSteps \} = calculateTestStats\(\);", 
"""  const totalUi = analysisResult?.estimatedUiTests || 47;
  const totalApi = analysisResult?.estimatedApiTests || 12;
  const testScenarios = analysisResult?.testScenarios || 226;
  const testSteps = analysisResult?.testSteps || 1256;
  const estimatedRuntimeMins = analysisResult?.estimatedRuntimeMins || 18;
  const confidenceScore = analysisResult?.confidenceScore || 98.5;
  const recommendedTool = analysisResult?.recommendedTestingTool || 'Playwright';
  const recommendedReasons = analysisResult?.recommendedToolReasons || ['Modern web application oriented', 'Fast execution and reliable', 'Cross-browser testing support', 'Auto-wait and smart assertions', 'High test stability and maintainability'];
  const coveragePrediction = analysisResult?.coveragePrediction || 95;""", front_content, flags=re.DOTALL)


front_content = front_content.replace("{['Modern web application oriented', 'Fast execution and reliable', 'Cross-browser testing support', 'Auto-wait and smart assertions', 'High test stability and maintainability'].map",
"{recommendedReasons.map")

front_content = front_content.replace("Playwright</h3>", "{recommendedTool}</h3>")
front_content = front_content.replace("95%", "{coveragePrediction}%")
front_content = front_content.replace("18 mins", "{estimatedRuntimeMins} mins")
front_content = front_content.replace("98.5%", "{confidenceScore}%")
front_content = front_content.replace('strokeDasharray="95, 100"', 'strokeDasharray={`${coveragePrediction}, 100`}')

with open(front_path, "w", encoding="utf-8") as f:
    f.write(front_content)

print("Done updating metrics!")
