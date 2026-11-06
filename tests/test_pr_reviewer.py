"""Offline tests of review routing/reporting; no model or GitHub call is made."""
import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('pr_reviewer', ROOT / '.github/scripts/ai-pr-reviewer.py')
reviewer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reviewer)


class ReviewerReportingTests(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ, {'PR_NUMBER': '18', 'BASE_REF': 'main',
                                     'PR_TITLE': 'Synthetic review', 'GH_TOKEN': 'fixture'}, clear=True)
        env.start()
        self.addCleanup(env.stop)
        for name, kwargs in (
            ('run_cmd', {'return_value': 'diff --git a/example.py b/example.py\n+changed'}),
            ('find_antigravity_agentapi', {'return_value': []}),
            ('load_file_safely', {'side_effect': lambda path: (ROOT/path).read_text(encoding='utf-8')}),
            ('post_github_comment', {'return_value': True}),
            ('call_github_models', {'return_value': ''}),
        ):
            mocker = patch.object(reviewer, name, **kwargs)
            setattr(self, name, mocker.start())
            self.addCleanup(mocker.stop)

    def test_unavailable_model_does_not_claim_harness_or_security_pass(self):
        reviewer.main()
        body = self.post_github_comment.call_args.args[1]
        self.assertIn('NOT_RUN', body)
        self.assertNotIn('통과 확인', body)
        self.assertIn('독립 보안', body)

    def test_prompt_uses_current_owner_mapping_and_relevant_capabilities(self):
        self.call_github_models.return_value = 'Synthetic review only.'
        reviewer.main()
        prompt = self.call_github_models.call_args.args[1]
        self.assertIn('Product Lead', prompt)
        self.assertIn('Quality Lead', prompt)
        self.assertIn('Delivery Lead', prompt)
        self.assertNotIn('8인', prompt)
        self.assertIn('비신뢰', prompt)
        self.assertIn('독립 보안', prompt)


if __name__ == '__main__':
    unittest.main()
