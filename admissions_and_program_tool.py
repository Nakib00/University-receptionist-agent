import json
from livekit.agents import function_tool, RunContext

# Data extracted from prompts.py
admission_info = {
    "undergraduate_admissions": {
      "ssc_hsc_and_equivalent": {
        "required_gpa": "Aggregate GPA of 7.0 in secondary and higher secondary level, with a minimum GPA of 3.00 in each."
      },
      "o_level_a_level_and_equivalent": {
        "o_level_requirements": "At least 5 subjects in O Level with a minimum GPA of 2.50.",
        "a_level_requirements": "At least 2 subjects in A Level with a minimum GPA of 2.00."
      }
    },
    "graduate_admissions": {
      "mba_emba_admission_requirements": {
        "mba_admission_requirements": {
          "academic_requirements": [
            "Three-year Bachelor Degree from a reputed university and at least one year of work experience.",
            "or",
            "Four-year Bachelor Degree from a reputed university. Some work experience after graduation in a managerial/executive position is preferable, but not essential.",
            "A CGPA of at least 2.50 at the undergraduate or graduate level with no 3rd Division/Class in any previous public examination."
          ],
          "test_requirements": "Acceptable score in the IUB Admission Test or score of 500 in GMAT."
        }
      }
    }
}

@function_tool()
async def get_undergraduate_admissions_info(
    context: RunContext,  # type: ignore
) -> str:
    """
    Provide the general requirements for undergraduate admission.
    """
    return json.dumps(admission_info.get("undergraduate_admissions", {}))

@function_tool()
async def get_graduate_admissions_info(
    context: RunContext,  # type: ignore
    program: str
) -> str:
    """
    Provide detailed admission requirements for specific graduate programs like MBA or MSc in Economics.
    """
    program_key = f"{program.lower().replace(' ', '_')}_admission_requirements"
    for key, value in admission_info.get("graduate_admissions", {}).items():
        if program.lower() in key:
            return json.dumps(value)
    return f"Admission information for {program} not found."