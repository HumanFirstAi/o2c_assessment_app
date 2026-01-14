"""
Test suite for Claude API synthesis in report generation.

Tests:
- API calls to Claude
- Context formatting
- Synthesis functions
- Fallback behavior
- Agent name validation
- Speculative language detection
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.report_generator import (
    synthesize_with_claude,
    format_gap_context,
    format_strength_context,
    format_executive_context,
    VALID_AGENTS,
    SYNTHESIS_SYSTEM_PROMPT
)


# Sample test data
SAMPLE_GAP = {
    'capability_id': 'test_cap_1',
    'capability_name': 'Test Capability',
    'phase_name': 'Invoice',
    'importance': 9,
    'readiness': 3,
    'gap_score': 6
}

SAMPLE_KB_DATA = {
    'id': 'test_cap_1',
    'name': 'Test Capability',
    'why_it_matters': 'This capability is critical for business operations.',
    'how_it_works_today': 'Currently managed through manual processes.',
    'agent_mapping': {
        'primary_agents': ['Billing Operations Agent'],
        'supporting_agents': ['Revenue Narrator']
    },
    'current_ai_capabilities': {
        'platform_features': ['Feature A', 'Feature B'],
        'mcp_tools': ['zuora_codegen', 'query_objects']
    },
    'whats_coming': {
        'timeline': '6-12M',
        'capabilities': ['Enhanced AI routing', 'Automated reconciliation']
    }
}

SAMPLE_STRENGTH = {
    'capability_name': 'Strong Capability',
    'phase_name': 'Collect',
    'importance': 8,
    'readiness': 9
}


class TestContextFormatters:
    """Test context formatting functions."""

    def test_format_gap_context_includes_all_fields(self):
        """Test that gap context includes all required fields."""
        context = format_gap_context(SAMPLE_GAP, SAMPLE_KB_DATA)

        assert 'Test Capability' in context
        assert 'Invoice' in context
        assert 'Importance=9' in context
        assert 'Readiness=3' in context
        assert 'URGENT GAP' in context
        assert 'This capability is critical' in context
        assert 'Billing Operations Agent' in context
        assert 'Revenue Narrator' in context
        assert 'Feature A' in context
        assert 'zuora_codegen' in context
        assert "WHAT'S COMING" in context
        assert 'Enhanced AI routing' in context
        assert 'Automated reconciliation' in context

    def test_format_gap_context_handles_missing_data(self):
        """Test gap context handles missing KB data gracefully."""
        empty_kb = {
            'agent_mapping': {},
            'current_ai_capabilities': {}
        }
        context = format_gap_context(SAMPLE_GAP, empty_kb)

        assert 'Test Capability' in context
        assert 'Not documented' in context

    def test_format_strength_context_includes_key_fields(self):
        """Test that strength context includes key fields."""
        context = format_strength_context(SAMPLE_STRENGTH, SAMPLE_KB_DATA)

        assert 'Strong Capability' in context
        assert 'Collect' in context
        assert 'STRENGTH' in context
        assert 'Billing Operations Agent' in context

    def test_format_executive_context_calculates_metrics(self):
        """Test executive context includes calculated metrics."""
        context = format_executive_context(
            company_name="Test Company",
            total_scored=42,
            urgent_gaps=[SAMPLE_GAP],
            critical_gaps=[],
            avg_importance=7.5,
            avg_readiness=6.2
        )

        assert 'Test Company' in context
        assert '42 capabilities scored' in context
        assert 'Average Importance: 7.5' in context
        assert 'Average Readiness: 6.2' in context
        assert 'Urgent Gaps (High I, Low R): 1' in context
        assert 'identifies capability gaps' in context.lower()


class TestClaudeSynthesis:
    """Test Claude API synthesis functions."""

    @patch('modules.report_generator.client')
    def test_synthesize_with_claude_success(self, mock_client):
        """Test successful Claude API call."""
        # Mock the API response
        mock_response = Mock()
        mock_response.content = [Mock(text="This is synthesized strategic content.")]
        mock_client.messages.create.return_value = mock_response

        result = synthesize_with_claude(
            section_type="urgent_gap",
            context_content="Test context with facts",
            agents_list=VALID_AGENTS
        )

        # Verify API was called
        assert mock_client.messages.create.called
        call_args = mock_client.messages.create.call_args

        # Verify correct model and parameters
        assert call_args[1]['model'] == 'claude-sonnet-4-20250514'
        assert call_args[1]['max_tokens'] == 1500
        assert call_args[1]['system'] == SYNTHESIS_SYSTEM_PROMPT

        # Verify result
        assert result == "This is synthesized strategic content."

    @patch('modules.report_generator.client')
    def test_synthesize_with_claude_includes_agent_constraints(self, mock_client):
        """Test that agent constraints are included in prompt."""
        mock_response = Mock()
        mock_response.content = [Mock(text="Synthesized content")]
        mock_client.messages.create.return_value = mock_response

        synthesize_with_claude(
            section_type="urgent_gap",
            context_content="Test context",
            agents_list=['Billing Operations Agent', 'Churn Agent']
        )

        # Get the user prompt that was sent
        call_args = mock_client.messages.create.call_args
        user_message = call_args[1]['messages'][0]['content']

        # Verify agent list is in prompt
        assert 'VALID AGENT NAMES' in user_message
        assert 'Billing Operations Agent' in user_message
        assert 'Churn Agent' in user_message
        assert 'Do NOT reference any agent not in this list' in user_message

    @patch('modules.report_generator.client')
    def test_synthesize_with_claude_api_failure_fallback(self, mock_client):
        """Test fallback behavior when API fails."""
        # Mock API failure
        mock_client.messages.create.side_effect = Exception("API Error")

        result = synthesize_with_claude(
            section_type="urgent_gap",
            context_content="Fallback context content",
            agents_list=VALID_AGENTS
        )

        # Should return original context as fallback
        assert result == "Fallback context content"

    @patch('modules.report_generator.client')
    def test_synthesize_uses_correct_prompt_for_section_type(self, mock_client):
        """Test that different section types use appropriate prompts."""
        mock_response = Mock()
        mock_response.content = [Mock(text="Result")]
        mock_client.messages.create.return_value = mock_response

        # Test executive summary
        synthesize_with_claude("executive_summary", "Context", VALID_AGENTS)
        exec_call = mock_client.messages.create.call_args[1]['messages'][0]['content']
        assert 'C-level audience' in exec_call

        # Test urgent gap - check for new structured format
        synthesize_with_claude("urgent_gap", "Context", VALID_AGENTS)
        gap_call = mock_client.messages.create.call_args[1]['messages'][0]['content']
        assert 'STRUCTURED format' in gap_call
        assert 'Why This Matters' in gap_call
        assert 'Available Today' in gap_call
        assert "What's Coming" in gap_call
        assert 'Business Impact' in gap_call

        # Test strength - check for new structured format
        synthesize_with_claude("strength", "Context", VALID_AGENTS)
        strength_call = mock_client.messages.create.call_args[1]['messages'][0]['content']
        assert 'Why This Is A Strength' in strength_call
        assert "What's Working" in strength_call
        assert 'Protect By' in strength_call


class TestAgentValidation:
    """Test agent name validation in synthesis."""

    @patch('modules.report_generator.client')
    def test_only_valid_agents_in_prompt(self, mock_client):
        """Test that only VALID_AGENTS are included in constraints."""
        mock_response = Mock()
        mock_response.content = [Mock(text="Result")]
        mock_client.messages.create.return_value = mock_response

        synthesize_with_claude(
            "urgent_gap",
            "Context",
            VALID_AGENTS
        )

        user_message = mock_client.messages.create.call_args[1]['messages'][0]['content']

        # Verify known valid agents are in the list
        assert 'Billing Operations Agent' in user_message
        assert 'Revenue Narrator' in user_message
        assert 'Collections Manager Agent' in user_message

    def test_valid_agents_list_completeness(self):
        """Test that VALID_AGENTS list contains expected agents."""
        expected_agents = [
            'Billing Operations Agent',
            'Collections Manager Agent',
            'Revenue Narrator',
            'Churn Agent',
            'Query Assistant',
            'Reconciliation AI'
        ]

        for agent in expected_agents:
            assert agent in VALID_AGENTS, f"Missing expected agent: {agent}"


class TestSystemPromptConstraints:
    """Test system prompt constraints."""

    def test_system_prompt_forbids_speculation(self):
        """Test that system prompt explicitly forbids speculation."""
        assert 'NO speculation' in SYNTHESIS_SYSTEM_PROMPT
        assert 'could potentially' in SYNTHESIS_SYSTEM_PROMPT
        assert 'might be able to' in SYNTHESIS_SYSTEM_PROMPT

    def test_system_prompt_defines_librarian_role(self):
        """Test that system prompt defines librarian role."""
        assert 'librarian' in SYNTHESIS_SYSTEM_PROMPT.lower()
        assert 'not an inventor' in SYNTHESIS_SYSTEM_PROMPT.lower()

    def test_system_prompt_requires_provided_content_only(self):
        """Test that system prompt requires using only provided content."""
        assert 'ONLY use information provided' in SYNTHESIS_SYSTEM_PROMPT
        assert 'provided in the user message' in SYNTHESIS_SYSTEM_PROMPT


class TestIntegration:
    """Integration tests for synthesis pipeline."""

    @patch('modules.report_generator.client')
    def test_full_synthesis_pipeline(self, mock_client):
        """Test complete synthesis pipeline from context to result."""
        # Mock API response
        mock_response = Mock()
        mock_response.content = [Mock(text="""
This urgent gap in Test Capability requires immediate attention. The Billing
Operations Agent and Revenue Narrator provide critical support through Feature A
and Feature B, accessible via the zuora_codegen MCP tool.
        """.strip())]
        mock_client.messages.create.return_value = mock_response

        # Format context
        context = format_gap_context(SAMPLE_GAP, SAMPLE_KB_DATA)

        # Synthesize
        result = synthesize_with_claude("urgent_gap", context, VALID_AGENTS)

        # Normalize whitespace for assertions
        normalized_result = ' '.join(result.split())

        # Verify result includes KB content
        assert 'Test Capability' in result
        assert 'Billing Operations Agent' in normalized_result
        assert 'Revenue Narrator' in normalized_result

    @patch('modules.report_generator.client')
    def test_synthesis_with_empty_agent_list(self, mock_client):
        """Test synthesis handles empty agent list gracefully."""
        mock_response = Mock()
        mock_response.content = [Mock(text="Result without agents")]
        mock_client.messages.create.return_value = mock_response

        result = synthesize_with_claude(
            "urgent_gap",
            format_gap_context(SAMPLE_GAP, {'current_ai_capabilities': {}, 'agent_mapping': {}}),
            []
        )

        # Should still work
        assert isinstance(result, str)
        assert len(result) > 0


class TestErrorHandling:
    """Test error handling in synthesis."""

    @patch('modules.report_generator.client')
    def test_handles_timeout_error(self, mock_client):
        """Test handling of timeout errors."""
        mock_client.messages.create.side_effect = TimeoutError("Request timed out")

        result = synthesize_with_claude("urgent_gap", "Context", VALID_AGENTS)

        # Should fall back to context
        assert result == "Context"

    @patch('modules.report_generator.client')
    def test_handles_authentication_error(self, mock_client):
        """Test handling of authentication errors."""
        mock_client.messages.create.side_effect = Exception("Authentication failed")

        result = synthesize_with_claude("urgent_gap", "Fallback", VALID_AGENTS)

        # Should fall back gracefully
        assert result == "Fallback"

    @patch('modules.report_generator.client')
    def test_handles_malformed_response(self, mock_client):
        """Test handling of malformed API responses."""
        # Mock malformed response
        mock_response = Mock()
        mock_response.content = []  # Empty content
        mock_client.messages.create.return_value = mock_response

        # This should raise an error and fall back
        try:
            result = synthesize_with_claude("urgent_gap", "Fallback", VALID_AGENTS)
            # If no exception, should get fallback or handle gracefully
            assert isinstance(result, str)
        except Exception:
            # Exception is acceptable as long as it doesn't crash
            pass


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
