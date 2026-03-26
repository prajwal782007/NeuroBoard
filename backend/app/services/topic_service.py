from app.models.topic_model import TopicRequest, TopicResponse
try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:
    pass # Managed safely through Docker production deployment

class TopicService:
    def __init__(self):
        """
        Initializes an embedded NLP Semantic Search configuration.
        """
        # Load a high-performance semantic transformer 
        self.model = SentenceTransformer('all-MiniLM-L6-v2') 
        
        # Core instructional mapping
        self.knowledge_base = {
            "Electromagnetic Radiation": ["electromagnetic spectrum", "wave propagation diagram", "photon reflection map"],
            "Photosynthesis": ["chloroplast structure", "calvin cycle flowchart", "light-dependent reactions"],
            "System Architecture": ["microservices overview", "database UML model", "load balancer schema"],
            "Neural Networks": ["multi-layer perceptron outline", "activation function curves", "backpropagation sequence"]
        }
        
        self.kb_titles = list(self.knowledge_base.keys())
        self.kb_embeddings = self.model.encode(self.kb_titles)

    def analyze_topic(self, request: TopicRequest) -> TopicResponse:
        title = request.title.strip()
        if not title:
            return TopicResponse(topic="unknown", suggestions=[])
            
        # Encode user string
        query_emb = self.model.encode(title)
        
        # Compute cosine similarities via NLP
        cosine_scores = util.cos_sim(query_emb, self.kb_embeddings)[0]
        
        # Retrieve highest matched trajectory
        best_idx = int(cosine_scores.argmax())
        best_score = float(cosine_scores[best_idx])
        
        # Provide confident suggestions
        if best_score > 0.4:
            matched_topic = self.kb_titles[best_idx]
            suggestions = self.knowledge_base[matched_topic]
            return TopicResponse(topic=matched_topic, suggestions=suggestions)
            
        return TopicResponse(
            topic=title,
            suggestions=["brainstorming mind map", "blank conceptual flowchart"]
        )
