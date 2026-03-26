from app.models.math_model import MathRequest, MathResponse
from app.ai.math_recognition.recognizer import MathRecognizer
from app.ai.math_recognition.solver import MathSolver

class MathService:
    def __init__(self):
        self.recognizer = MathRecognizer()
        self.solver = MathSolver()

    def process_math(self, request: MathRequest) -> MathResponse:
        try:
            # 1. Extract text from sketch image via OCR
            equation_text = self.recognizer.extract_text(request.image_base64)
            if not equation_text:
                return MathResponse(equation="", solution="", error="Could not detect equation in image")

            # 2. Solve the expression symmetrically
            solution = self.solver.solve(equation_text)
            
            return MathResponse(
                equation=equation_text,
                solution=solution
            )
        except Exception as e:
            return MathResponse(equation="", solution="", error=str(e))
