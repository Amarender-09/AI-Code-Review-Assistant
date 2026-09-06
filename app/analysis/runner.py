import logging

from app.analysis.base import Analyzer
from app.models.finding import Finding


logger = logging.getLogger(__name__)


class AnalyzerRunner:

    def __init__(self, analyzers: list[Analyzer]):
        self.analyzers = analyzers

    def run(
        self,
        source_code: str,
        file_path: str,
    ) -> tuple[list[Finding], list[str]]:

        findings = []
        warnings = []

        for analyzer in self.analyzers:

            analyzer_name = analyzer.__class__.__name__

            try:
                analyzer_findings = analyzer.analyze(
                    source_code,
                    file_path,
                )

                findings.extend(analyzer_findings)

            except Exception as error:
                warning = (
                    f"{analyzer_name} failed: {error}"
                )

                logger.exception(warning)

                warnings.append(warning)

        return findings, warnings