"""
Transcript Agent - Processes raw meeting transcripts into structured notes
"""
from typing import Dict, Any
from .base_agent import BaseAgent, AgentConfig, AgentResult
import json


class IntakeAgent(BaseAgent):
    """
    Agent responsible for processing raw transcripts into structured notes
    Extracts: Company profile, attendees, objectives, discussion points, action items
    """
    
    def __init__(self, llm_client):
        config = AgentConfig(
            name="IntakeAgent",
            description="Processes raw meeting transcripts into structured notes",
            model="z-ai/glm-4.6",  # GLM-4.6 via OpenRouter
            temperature=0.3,  # Lower temperature for factual extraction
            max_tokens=12000
        )
        super().__init__(config, llm_client)
    
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        Process transcript and extract structured information
        
        Input:
            - transcript: Raw meeting transcript text
            - project_name: Name of the project
            
        Output:
            - structured_notes: Dict with structured meeting information
        """
        try:
            self.log_execution("start", "Processing transcript")
            self.validate_input(input_data, ["transcript", "project_name"])
            
            transcript = input_data["transcript"]
            project_name = input_data["project_name"]
            
            # Create prompt for extracting structured notes
            system_message = """You are an expert at analyzing meeting transcripts and extracting structured information.
Your task is to carefully read meeting transcripts and extract key information in a well-organized format."""
            
            user_message = f"""Analyze the following meeting transcript and extract structured information.

Project Name: {project_name}

Transcript:
{transcript}

Please extract and structure the following information in JSON format:
1. company_overview: Brief description of the company/organization (if mentioned)
2. attendees: List of people who attended the meeting (if mentioned)
3. meeting_date: Date of meeting (if mentioned, or "Not specified")
4. meeting_objective: Main purpose/goal of the meeting
5. key_discussion_points: List of main topics discussed (at least 5-7 points)
6. pain_points: List of challenges or problems identified
7. requirements: List of key requirements or needs mentioned
8. decisions_made: List of decisions or conclusions reached
9. action_items: List of follow-up actions (if any)
10. technical_constraints: Any technical limitations or constraints mentioned
11. stakeholders: Key stakeholders mentioned

Return ONLY valid JSON without any markdown formatting or explanations. The JSON should be parseable directly."""

            self.log_execution("llm_call", "Extracting structured information")
            response = await self._call_llm(system_message, user_message, max_retries=3)

            # Parse JSON response using robust parser
            structured_notes = self.parse_json_response(response, fallback_key="raw_response")

            # Check if parsing was successful
            has_parse_error = "parse_error" in structured_notes

            self.log_execution(
                "success" if not has_parse_error else "warning",
                f"Extracted {len(structured_notes)} fields" + (" (with parse warnings)" if has_parse_error else "")
            )

            return AgentResult(
                success=True,
                data={
                    "structured_notes": structured_notes,
                    "project_name": project_name,
                    "transcript_length": len(transcript)
                },
                metadata={
                    "agent": self.config.name,
                    "fields_extracted": list(structured_notes.keys()),
                    "parse_warning": has_parse_error
                }
            )
                
        except Exception as e:
            self.logger.error(f"Error in TranscriptAgent: {str(e)}")
            return AgentResult(
                success=False,
                data=None,
                error=str(e),
                metadata={"agent": self.config.name}
            )
