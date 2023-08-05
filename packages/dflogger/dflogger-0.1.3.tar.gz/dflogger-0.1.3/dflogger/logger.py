import pandas as pd
import logging


class Logger:
    def __init__(self):
        self.active = True
        self._df = None

        # default logging level
        logging.basicConfig(level=logging.INFO)

    def set_logger_level(self, level: str) -> None:
        if level == "debug":
            logging.basicConfig(level=logging.DEBUG)
        elif level == "info":
            logging.basicConfig(level=logging.INFO)
        elif level == "warning":
            logging.basicConfig(level=logging.WARNING)
        elif level == "error":
            logging.basicConfig(level=logging.ERROR)
        elif level == "critical":
            logging.basicConfig(level=logging.CRITICAL)
        else:
            raise Exception("Invalid logging level")

    def log(self, run_name: str, params: dict, metrics: dict) -> None:
        if not self.active:
            raise Exception("Logger is not active")

        parsed_params = {f"param_{k}": v for k, v in params.items()}
        parsed_metrics = {f"metric_{k}": v for k, v in metrics.items()}

        logging.info(
            f"Run: {run_name} | Params: {parsed_params} | Metrics: {parsed_metrics}")

        if self._df is None:
            self._df = pd.DataFrame({
                "run": [run_name],
                **parsed_params,
                **parsed_metrics
            })

        else:
            df_temp = pd.DataFrame({
                "run": [run_name],
                **parsed_params,
                **parsed_metrics
            })
            self._df = pd.concat(
                [
                    self._df,
                    df_temp
                ], ignore_index=True
            )

    def finish(self):
        self.active = False

    def best_score(self, metric: str) -> float:
        if not self.active:
            raise Exception("Logger is not active")

        try:
            best_score = self._df[f"metric_{metric}"].max()
        except:
            best_score = self._df[f"{metric}"].max()

        return best_score

    def best_params(self, metric: str) -> dict:
        if not self.active:
            raise Exception("Logger is not active")

        try:
            best_run = self._df[self._df[f"metric_{metric}"] == self.best_score(
                metric)]["run"].values[0]
        except:
            best_run = self._df[self._df[f"{metric}"] == self.best_score(
                metric)]["run"].values[0]

        params = self._df[self._df["run"] == best_run].iloc[0] \
            .drop([metric for metric in self._df.columns if "metric" in metric]) \
            .drop(["run"]) \

        params.index = [col.split("_", 1)[1] for col in params.index]
        params = params.to_dict()

        return params

    def get_df(self) -> pd.DataFrame:
        clean_col = [
            " ".join(col.split("_", 1)[1:]) if "_" in col else col for col in self._df.columns
        ]
        df_temp = self._df.copy()
        df_temp.columns = clean_col

        return df_temp

    def get_df_raw(self) -> pd.DataFrame:
        return self._df

    def to_csv(self, path="dflogger", raw=False, index=False):
        if raw:
            self._df.to_csv(path, index=index)
        else:
            self.get_df().to_csv(path, index=index)
