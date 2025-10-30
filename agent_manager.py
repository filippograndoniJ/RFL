import openai, subprocess, os, glob
openai.api_key = os.getenv("OPENAI_API_KEY")

def quick_test(code_path, sample_input, expected_output):
    result = subprocess.run(
        ["python", code_path],
        input=sample_input.encode(),
        capture_output=True,
        text=True,
        timeout=4
    )
    passed = result.stdout.strip() == expected_output.strip()
    return passed, result.stdout, result.stderr

def solve_problem(problem_txt, input_txt, output_txt, sol_path):
    problem_text = open(problem_txt).read()
    sample_input = open(input_txt).read()
    expected_output = open(output_txt).read()

    prompt = f"""
You are a competitive programming assistant.
Write efficient Python 3 code solving the problem below.
Read input from stdin and print output to stdout.

Problem:
{problem_text}
"""

    print(f"🧠 Solving {problem_txt} ...")
    code = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.2,
        max_tokens=1000
    ).choices[0].message.content
    open(sol_path,"w").write(code)

    ok, out, err = quick_test(sol_path, sample_input, expected_output)
    print("AI output:\n", out)
    if ok:
        print("✅ Sample passed!\n")
    else:
        print("❌ Sample failed, paste this into Cursor chat:\n", err[:500],"\n")

# Main loop
for i, problem_txt in enumerate(sorted(glob.glob("problems/problem*.txt")), start=1):
    solve_problem(
        problem_txt,
        f"samples/p{i}_input.txt",
        f"samples/p{i}_output.txt",
        f"workspace/solution{i}.py"
    )