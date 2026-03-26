from app.models.diagram_model import DiagramRequest, DiagramResponse

class DiagramService:
    def generate_mermaid(self, request: DiagramRequest) -> DiagramResponse:
        """
        Converts structured canvas elements into Mermaid.js compatible semantic markup.
        """
        lines = ["graph TD"]
        
        # 1. Map element types to Mermaid shapes
        for el in request.elements:
            # Fallback label to type if none provided
            lbl = el.label if el.label else el.type.capitalize()
            
            # Sanitize labels
            lbl = lbl.replace('"', '').replace('(', '').replace(')', '')
            
            if el.type.lower() == "circle":
                lines.append(f"    {el.id}(({lbl}))")
            elif el.type.lower() == "diamond":
                lines.append(f"    {el.id}{{{lbl}}}")
            else:
                # Default to rectangle
                lines.append(f"    {el.id}[{lbl}]")
                
        # 2. Add structural directional connections
        for conn in request.connections:
            if conn.label:
                lbl = conn.label.replace('"', '')
                lines.append(f"    {conn.source_id} -- \"{lbl}\" --> {conn.target_id}")
            else:
                lines.append(f"    {conn.source_id} --> {conn.target_id}")
                
        mermaid_code = "\n".join(lines)
        return DiagramResponse(mermaid_code=mermaid_code)
