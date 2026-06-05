import pytest
from orchestrator.workflow import WorkflowOrchestrator
from pathlib import Path

class TestWorkflowOrchestrator:
    
    @pytest.mark.asyncio
    async def test_process_email_with_order_issue(self):
        """Test: Email with only order issue"""
        orchestrator = WorkflowOrchestrator()
        result = await orchestrator.process("My order #1234 is late")
        
        assert result.metadata["success"] is True
        assert result.metadata["intent_count"] >= 1
        assert "order" in result.final_response.lower()
    
    @pytest.mark.asyncio
    async def test_process_email_with_technical_issue(self):
        """Test: Email with only technical issue"""
        orchestrator = WorkflowOrchestrator()
        result = await orchestrator.process("My speaker won't connect")
        
        assert result.metadata["success"] is True
        # Check if technical intent was detected
        technical_steps = [s for s in result.processing_steps if s.department and s.department.value == "technical"]
        assert len(technical_steps) > 0
    
    @pytest.mark.asyncio
    async def test_process_email_with_refund_request(self):
        """Test: Email with refund request"""
        orchestrator = WorkflowOrchestrator()
        result = await orchestrator.process("I want a refund")
        
        assert result.metadata["success"] is True
        assert "refund" in result.final_response.lower()
    
    @pytest.mark.asyncio
    async def test_process_email_with_multiple_intents(self):
        """Test: Email with all three issues"""
        orchestrator = WorkflowOrchestrator()
        email = "My order #1234 is late, speaker broken, need refund"
        result = await orchestrator.process(email)
        
        assert result.metadata["success"] is True
        assert result.metadata["intent_count"] == 3
        assert all(dep in result.metadata["departments_involved"] 
                   for dep in ["sales", "technical", "finance"])
        

    @pytest.mark.asyncio
    async def test_complex_email(self):
        # Load email from file
        examples_dir = Path(__file__).parent.parent / "examples"
        email = (examples_dir / "complex_email.txt").read_text()
      
        orchestrator = WorkflowOrchestrator()
        result = await orchestrator.process(email)
      
        # Assertions
        assert result.metadata["success"] is True
        assert result.metadata["intent_count"] == 3
        assert "order" in result.final_response.lower()
        assert "speaker" in result.final_response.lower()
        assert "refund" in result.final_response.lower()
    
    @pytest.mark.asyncio
    async def test_health_check(self):
        """Test: Health endpoint logic"""
        from main import health_check
        response = await health_check()
        assert response["status"] == "healthy"
        assert response["model"] == "llama3.2:3b"