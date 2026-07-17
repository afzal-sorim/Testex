import os

base_dir = r"c:\Users\ST-Balakumaran\Downloads\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\frontend\src\pages"

ai_test_path = os.path.join(base_dir, "AITestRecommendation.jsx")
with open(ai_test_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("analysisResult?.estimatedUiTests || 47", "analysisResult?.estimatedUiTests || 0")
content = content.replace("analysisResult?.estimatedApiTests || 12", "analysisResult?.estimatedApiTests || 0")
content = content.replace("analysisResult?.testScenarios || 226", "analysisResult?.testScenarios || 0")
content = content.replace("analysisResult?.testSteps || 1256", "analysisResult?.testSteps || 0")
content = content.replace("analysisResult?.estimatedRuntimeMins || 18", "analysisResult?.estimatedRuntimeMins || 0")
content = content.replace("analysisResult?.confidenceScore || 98.5", "analysisResult?.confidenceScore || 0")
content = content.replace("analysisResult?.coveragePrediction || 95", "analysisResult?.coveragePrediction || 0")
content = content.replace("analysisResult?.existingTestCount || 152", "analysisResult?.existingTestCount || 0")
content = content.replace("analysisResult?.existingTestPassed || 74", "analysisResult?.existingTestPassed || 0")
content = content.replace("analysisResult?.existingTestFailed || 0", "analysisResult?.existingTestFailed || 0")

with open(ai_test_path, "w", encoding="utf-8") as f:
    f.write(content)

func_test_path = os.path.join(base_dir, "FunctionalTesting.jsx")
with open(func_test_path, "r", encoding="utf-8") as f:
    content2 = f.read()

content2 = content2.replace("result?.testScenarios || 226", "result?.testScenarios || 0")

with open(func_test_path, "w", encoding="utf-8") as f:
    f.write(content2)

print("Consistency updated successfully.")
