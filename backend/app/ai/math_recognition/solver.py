import sympy

class MathSolver:
    def solve(self, equation_text: str) -> str:
        """
        Parses OCR text and returns a solved string using sympy.
        """
        # Clean text
        text = equation_text.replace('=', '').replace('×', '*').strip()
        
        if not text:
            return ""

        try:
            # Check if there's an algebraic variable
            if 'x' in text.lower() or 'y' in text.lower():
                # For algebraic equations (e.g. x**2 + 4 = 0), sympy.sympify treats it as expression == 0
                expr = sympy.sympify(text)
                
                # Retrieve the variable to solve for
                syms = list(expr.free_symbols)
                if syms:
                    roots = sympy.solve(expr, syms[0])
                    # Format the roots gracefully
                    return ", ".join([str(root) for root in roots])
            
            # Fallback arithmetic evaluation (e.g. 2 + 2)
            expr = sympy.sympify(text)
            result = float(expr.evalf())
            
            # Format cleanly for integers
            if result.is_integer():
                return str(int(result))
            return str(round(result, 4))
            
        except Exception as e:
            return f"Error computing: {str(e)}"
