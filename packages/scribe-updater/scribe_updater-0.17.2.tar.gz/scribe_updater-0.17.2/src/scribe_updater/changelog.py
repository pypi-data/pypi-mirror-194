import json
import os


class ChangeLog:
    def __init__(
        self,
        ground_scenarios,
        target_scenarios,
        ground_competencies,
        target_competencies,
        special_products,
        output,
        ground_to_target_map,
    ):
        self.ground_scenarios = ground_scenarios
        self.ground_competencies = ground_competencies
        self.target_competencies = target_competencies
        self.target_scenarios = target_scenarios
        self.output = output
        self.products = special_products
        self.change_log = {"added": {}, "removed": {}, "moved": []}
        self.ground_to_target_map = ground_to_target_map

    def log_competency_added(self, competency, scenarios: dict):
        s = list(scenarios.keys())
        if not self.change_log["added"].get(competency, []):
            self.change_log["added"][competency] = s

    def log_scenario_added(self, competency, scenario):
        if "straight bussin" in scenario:
            return

        if not self.change_log["added"].get(competency, []):
            self.change_log["added"][competency] = [scenario]
        else:
            self.change_log["added"][competency].append(scenario)

    def log_competency_removed(self, competency, scenarios: dict):
        s = list(scenarios.keys())
        if not self.change_log["removed"].get(competency, {}):
            self.change_log["removed"][competency] = s

    def log_scenario_removed(self, competency, scenario):
        if not self.change_log["removed"].get(competency, []):
            self.change_log["removed"][competency] = [scenario]
        else:
            self.change_log["removed"][competency].append(scenario)

    def log_scenario_changed(self, competency, scenario, field):
        if field == "mapped":
            old_competency = self.ground_to_target_map[
                f"{competency}-*-{scenario}"
            ].split("-*-")[0]
            old_scenario = self.ground_to_target_map[
                f"{competency}-*-{scenario}"
            ].split("-*-")[1]
            self.change_log["moved"].append(
                {
                    "from": f"{old_competency}-*-{old_scenario}",
                    "to": f"{competency}-*-{scenario}",
                }
            )

    def check_for_removed_competencies_scenarios(self):
        for competency in self.target_scenarios:
            base_mapped = [
                value
                for value in [
                    self.ground_to_target_map[key]
                    for key in self.ground_to_target_map
                    if competency in key
                ]
                if "base" in value
            ]
            if (
                competency not in self.ground_scenarios
                and not base_mapped
                and competency not in ["disabled", "out_of_scope"]
            ):
                self.log_competency_removed(
                    competency, self.target_scenarios[competency]
                )
            else:
                for scenario in self.target_scenarios[competency]:
                    target_mapped = [
                        value
                        for value in self.ground_to_target_map.values()
                        if competency in value and scenario in value
                    ]
                    if (
                        scenario not in self.ground_scenarios.get(competency, [])
                        and not target_mapped
                        and scenario not in self.products.get(competency, [])
                        and competency not in ["disabled", "out_of_scope"]
                    ):
                        self.log_scenario_removed(competency, scenario)

    def check_for_added_competencies_scenarios(self):
        for competency in self.ground_scenarios:
            if competency not in self.target_scenarios:
                self.log_competency_added(competency, self.ground_scenarios[competency])
            else:
                for scenario in self.ground_scenarios[competency]:
                    output_key = competency + "-*-" + scenario
                    if (
                        scenario not in self.target_scenarios[competency]
                        and output_key not in self.ground_to_target_map.keys()
                    ):
                        self.log_scenario_added(competency, scenario)

                for scenario in self.products.get(competency, []):
                    if scenario not in self.target_scenarios.get(competency, []):
                        self.log_scenario_added(competency, scenario)

    def check_for_changed_competencies_scenarios(self):
        for competency in self.output["competencies"]:
            if competency["name"] in self.target_scenarios:
                if not competency["scenarios"]:
                    return
                for scenario in competency["scenarios"]:
                    output_key = competency["name"] + "-*-" + scenario["name"]
                    competency_scenario = self.ground_to_target_map.get(
                        output_key, ""
                    ).split("-*-")
                    target_mapped = (
                        len(competency_scenario) == 2
                        and competency_scenario[0] in self.target_scenarios
                        and competency_scenario[1]
                        in self.target_scenarios[competency_scenario[0]]
                    )
                    if target_mapped:
                        self.log_scenario_changed(
                            competency["name"], scenario["name"], "mapped"
                        )
            elif [
                value
                for value in [
                    self.ground_to_target_map[key]
                    for key in self.ground_to_target_map
                    if competency["name"] in key
                ]
                if "base" in value
            ]:
                for scenario in competency["scenarios"]:
                    output_key = competency["name"] + "-*-" + scenario["name"]
                    competency_scenario = self.ground_to_target_map.get(
                        output_key, ""
                    ).split("-*-")
                    target_mapped = (
                        len(competency_scenario) == 2
                        and competency_scenario[0] in self.target_scenarios
                        and competency_scenario[1]
                        in self.target_scenarios[competency_scenario[0]]
                    )
                    if target_mapped:
                        self.log_scenario_changed(
                            competency["name"], scenario["name"], "mapped"
                        )

    def check_for_removed_added_competencies_scenarios(self):
        self.check_for_removed_competencies_scenarios()
        self.check_for_added_competencies_scenarios()
        self.check_for_changed_competencies_scenarios()

    def create_change_log(self):
        self.check_for_removed_added_competencies_scenarios()
        return self.change_log

    def display_change_log(self):
        print(json.dumps(self.change_log, indent=2))

    def write_change_log_to_file(self):
        if not os.path.isdir("results"):
            os.mkdir("results")

        with open("results/diff_log.json", "w") as f:
            f.write(json.dumps(self.change_log, indent=4))
