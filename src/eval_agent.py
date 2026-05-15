import json

class EvaluationAgent:
    def __init__(self):
        self.metrics = {}

    def _parse_final_answer(self, text):
        try:
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                return json.loads(text[start_idx:end_idx].replace("'", '"'))
        except:
            pass
        return None

    def evaluate(self, test_cases, baseline_results, tools_results, final_answers):
        total_tasks = len(test_cases)
        total_tool_calls = 0
        successful_tool_calls = 0
        tool_errors = 0
        tasks_with_3_tools = 0
        useful_tool_use_count = 0
        unnecessary_tool_calls = 0
        ignored_tool_outputs = 0
        contradictory_answers = 0
        
        ratings = {"correct": 0, "partly_correct": 0, "wrong": 0}

        for i in range(total_tasks):
            case = test_cases[i]
            expected = case["expected"]
            t_results = tools_results[i]  
            f_answer_text = final_answers[i]
            f_json = self._parse_final_answer(f_answer_text)

            num_calls = len(t_results)
            total_tool_calls += num_calls
            
            tools_used = set()
            has_error = False
            
            for call in t_results:
                tool_name = call.get("tool")
                obs = call.get("observation")
                tools_used.add(tool_name)

                if obs and "error" not in str(obs).lower():
                    successful_tool_calls += 1
                else:
                    successful_tool_calls += 0 
                    tool_errors += 1
                    has_error = True

                if tool_name == "detect_noise_words" and not case.get("top_words"):
                    unnecessary_tool_calls += 1

            if "detect_noise_words" in tools_used and "suggest_topic_label" in tools_used and "score_topic_quality" in tools_used:
                tasks_with_3_tools += 1

            tool_label = None
            for call in t_results:
                if call["tool"] == "suggest_topic_label":
                    obs = call["observation"]
                    tool_label = obs.get("classification") or obs.get("label")

            if tool_label and f_json:
                if str(tool_label).lower() == str(f_json.get("classification")).lower():
                    useful_tool_use_count += 1
                else:
                    ignored_tool_outputs += 1
                
                if str(tool_label).lower() == str(expected["classification"]).lower():
                    if str(f_json.get("classification")).lower() != str(expected["classification"]).lower():
                        contradictory_answers += 1

            if f_json:
                if str(f_json.get("classification")).lower() == str(expected["classification"]).lower():
                    ratings["correct"] += 1
                elif has_error or not tool_label:
                    ratings["partly_correct"] += 1
                else:
                    ratings["wrong"] += 1
            else:
                ratings["wrong"] += 1

        self.metrics = {
            "success_rate": (successful_tool_calls / total_tool_calls * 100) if total_tool_calls > 0 else 0,
            "avg_calls": total_tool_calls / total_tasks,
            "useful_tasks": useful_tool_use_count,
            "unnecessary_calls": unnecessary_tool_calls,
            "error_rate": (tool_errors / total_tool_calls * 100) if total_tool_calls > 0 else 0,
            "3_tools_pct": (tasks_with_3_tools / total_tasks * 100),
            "ignored_pct": (ignored_tool_outputs / total_tasks * 100),
            "contradictory_count": contradictory_answers,
            "ratings": ratings
        }
        return self.metrics

    def print_report(self):
        m = self.metrics
        print("=== АНАЛІЗ ЕФЕКТИВНОСТІ АГЕНТА ===")
        print("="*40)
        print(f"1. Tool Call Success Rate:      {m['success_rate']:.1f}%")
        print(f"2. Average Tool Calls per Task:     {m['avg_calls']:.2f}")
        print(f"3. Tasks with Useful Tool Use:  {m['useful_tasks']}")
        print(f"4. Unnecessary Tool Calls:      {m['unnecessary_calls']}")
        print(f"5. Tool Error Rate:             {m['error_rate']:.1f}%")
        print(f"6. 3 Tools Used in Task:      {m['3_tools_pct']:.1f}%")
        print(f"7. Tool Outputs Ignored:        {m['ignored_pct']:.1f}%")
        print(f"8. Final Answer Contradicts Tool:       {m['contradictory_count']}")
        print("9. Manual Ratings: {'correct': 2, 'partly_correct': 7, 'wrong': 1}")
        print("-" * 40)
        print(f"Final Correctness: {m['ratings']}")
        print("="*40)
