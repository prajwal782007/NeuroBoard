import React, {
  useEffect,
  useRef,
  useImperativeHandle,
  forwardRef,
} from "react";
import { fabric } from "fabric";

/**
 * Fabric.js based CanvasBoard
 * Support for Drawing Shapes, Text, and "Cleaning" diagrams.
 */
const CanvasBoard = forwardRef(({ activeTool, brushColor, brushSize }, ref) => {
  const canvasElRef = useRef(null);
  const fabricRef = useRef(null);
  const containerRef = useRef(null);
  const drawingRef = useRef(null);

  // Initialize fabric canvas
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const canvas = new fabric.Canvas(canvasElRef.current, {
      width: container.offsetWidth,
      height: container.offsetHeight,
      backgroundColor: "#1e1e2e",
      selection: true,
    });
    fabricRef.current = canvas;

    // Resize handler
    const handleResize = () => {
      canvas.setWidth(container.offsetWidth);
      canvas.setHeight(container.offsetHeight);
      canvas.renderAll();
    };
    window.addEventListener("resize", handleResize);

    // Auto-solve math when text ends with "="
    canvas.on("text:changed", (opt) => {
      const obj = opt.target;
      if (!obj || obj.type !== "i-text") return;

      const text = obj.text.trim();
      if (text.endsWith("=") && text.length > 2) {
        const expression = text.slice(0, -1);
        try {
          // Safe-ish eval: only allow numbers, operators, and parentheses
          if (/^[0-9+\-*/().\s]+$/.test(expression)) {
            const result = eval(expression);
            
            // Add result text next to the original in "Shadows" style
            const resultText = new fabric.Text(result.toString(), {
              left: obj.left + obj.getBoundingRect().width + 20,
              top: obj.top,
              fontSize: 40,
              fill: "#3b82f6", // Bright blue marker
              fontFamily: "'Shadows Into Light', cursive",
              selectable: true,
              angle: Math.random() * 6 - 3,
            });
            
            canvas.add(resultText);
            canvas.renderAll();
          }
        } catch (e) {
          console.error("Math eval error", e);
        }
      }
    });

    return () => {
      window.removeEventListener("resize", handleResize);
      canvas.dispose();
    };
  }, []);

  // Update canvas state when tool changes
  useEffect(() => {
    const canvas = fabricRef.current;
    if (!canvas) return;

    // Reset common flags
    canvas.isDrawingMode = false;
    canvas.selection = false;
    canvas.defaultCursor = "default";
    canvas.forEachObject((o) => (o.selectable = false));

    // Clear previous event listeners
    canvas.off("mouse:down");
    canvas.off("mouse:move");
    canvas.off("mouse:up");

    switch (activeTool) {
      case "select":
        canvas.selection = true;
        canvas.forEachObject((o) => (o.selectable = true));
        canvas.defaultCursor = "default";
        break;

      case "pen":
        canvas.isDrawingMode = true;
        canvas.freeDrawingBrush.color = brushColor;
        canvas.freeDrawingBrush.width = brushSize * 1.5;
        break;

      case "eraser":
        canvas.defaultCursor = "crosshair";
        canvas.on("mouse:down", (opt) => {
          const target = canvas.findTarget(opt.e);
          if (target) {
            canvas.remove(target);
            canvas.renderAll();
          }
        });
        break;

      case "text":
        canvas.defaultCursor = "text";
        canvas.on("mouse:down", (opt) => {
          const pointer = canvas.getPointer(opt.e);
          const text = new fabric.IText("Type here", {
            left: pointer.x,
            top: pointer.y,
            fill: brushColor,
            fontSize: brushSize * 8,
            fontFamily: "'Inter', sans-serif",
            selectable: true,
          });
          canvas.add(text);
          canvas.setActiveObject(text);
          text.enterEditing();
          canvas.renderAll();
        });
        break;

      case "rectangle":
      case "circle":
      case "arrow":
        canvas.defaultCursor = "crosshair";
        canvas.on("mouse:down", handleShapeStart);
        canvas.on("mouse:move", handleShapeMove);
        canvas.on("mouse:up", handleShapeEnd);
        break;
      
      default:
        break;
    }

    canvas.renderAll();
  }, [activeTool, brushColor, brushSize]);

  // -- Shape Creation Handlers --

  function handleShapeStart(opt) {
    const canvas = fabricRef.current;
    const pointer = canvas.getPointer(opt.e);
    drawingRef.current = { startX: pointer.x, startY: pointer.y, shape: null };

    let shape;
    const shapeConfig = {
      fill: "transparent",
      stroke: brushColor,
      strokeWidth: brushSize,
      selectable: false,
    };

    if (activeTool === "rectangle") {
      shape = new fabric.Rect({
        ...shapeConfig,
        left: pointer.x,
        top: pointer.y,
        width: 0,
        height: 0,
      });
    } else if (activeTool === "circle") {
      shape = new fabric.Ellipse({
        ...shapeConfig,
        left: pointer.x,
        top: pointer.y,
        rx: 0,
        ry: 0,
      });
    } else if (activeTool === "arrow") {
      // Start with a line
      shape = new fabric.Line([pointer.x, pointer.y, pointer.x, pointer.y], {
        ...shapeConfig,
        id: "arrow-line",
      });
    }

    if (shape) {
      drawingRef.current.shape = shape;
      canvas.add(shape);
    }
  }

  function handleShapeMove(opt) {
    if (!drawingRef.current || !drawingRef.current.shape) return;
    const canvas = fabricRef.current;
    const pointer = canvas.getPointer(opt.e);
    const { startX, startY, shape } = drawingRef.current;

    if (activeTool === "rectangle") {
      shape.set({
        left: Math.min(startX, pointer.x),
        top: Math.min(startY, pointer.y),
        width: Math.abs(pointer.x - startX),
        height: Math.abs(pointer.y - startY),
      });
    } else if (activeTool === "circle") {
      shape.set({
        left: Math.min(startX, pointer.x),
        top: Math.min(startY, pointer.y),
        rx: Math.abs(pointer.x - startX) / 2,
        ry: Math.abs(pointer.y - startY) / 2,
      });
    } else if (activeTool === "arrow") {
      shape.set({ x2: pointer.x, y2: pointer.y });
    }

    shape.setCoords();
    canvas.renderAll();
  }

  function handleShapeEnd() {
    if (drawingRef.current && drawingRef.current.shape) {
      drawingRef.current.shape.set({ selectable: true });
    }
    drawingRef.current = null;
  }

  // --- NEW: Sketch to Shape Conversion Logic ---

  function processPath(obj) {
    if (!obj || obj.type !== "path") return;
    const canvas = fabricRef.current;
    if (!canvas) return;

    const bounds = obj.getBoundingRect();
    const w = bounds.width;
    const h = bounds.height;

    // Ignore tiny specks (less than 10px)
    if (w < 10 && h < 10) return;

    let shape;
    const baseStyle = {
      left: bounds.left,
      top: bounds.top,
      fill: "transparent",
      stroke: "white", // Dark theme friendly, or use obj.stroke
      strokeWidth: 2,
      selectable: true,
    };

    /**
     * User's Rules:
     * 1. |w - h| < 20 -> Circle
     * 2. h < 15 -> Horizontal Line
     * 3. Else -> Rectangle
     */
    if (Math.abs(w - h) < 20) {
      // It's a Circle
      const radius = Math.max(w, h) / 2;
      shape = new fabric.Circle({
        ...baseStyle,
        radius: radius,
      });
    } else if (h < 15) {
      // It's a Horizontal Line
      shape = new fabric.Line([bounds.left, bounds.top + h / 2, bounds.left + w, bounds.top + h / 2], {
        ...baseStyle,
      });
    } else {
      // It's a Rectangle
      shape = new fabric.Rect({
        ...baseStyle,
        width: w,
        height: h,
      });
    }

    if (shape) {
      canvas.remove(obj);
      canvas.add(shape);
      canvas.setActiveObject(shape);
      canvas.renderAll();
    }
  }

  // Use reach to expose methods to parent (App.jsx)
  useImperativeHandle(ref, () => ({
    addText(content, x, y) {
      const canvas = fabricRef.current;
      if (!canvas) return;
      const text = new fabric.Text(content, {
        left: x,
        top: y,
        fill: "#a6e3a1",
        fontSize: 50,
        fontFamily: "'Permanent Marker', cursive",
        selectable: true,
      });
      canvas.add(text);
      canvas.centerObject(text);
      canvas.renderAll();
    },

    clearCanvas() {
      const canvas = fabricRef.current;
      if (!canvas) return;
      canvas.clear();
      canvas.setBackgroundColor("#1e1e2e", () => canvas.renderAll());
    },

    async solveSketchMath(apiUrl) {
      const canvas = fabricRef.current;
      if (!canvas) return;

      // Get canvas data as image
      const dataURL = canvas.toDataURL({
        format: "png",
        multiplier: 1,
      });

      try {
        const res = await fetch(`${apiUrl}/solve-sketch`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ image: dataURL }),
        });
        const data = await res.json();
        if (data.error) throw new Error(data.error);

        // Calculate where to place the result (next to the paths)
        const paths = canvas.getObjects().filter(o => o.type === "path");
        let rightmost = canvas.getWidth() / 2;
        let topMost = canvas.getHeight() / 2;

        if (paths.length > 0) {
          const group = new fabric.Group(paths);
          const bounds = group.getBoundingRect();
          rightmost = bounds.left + bounds.width + 25;
          topMost = bounds.top - 10;
          group.destroy(); // DON'T group them permanently
        }

        // Add result text in a "Shadows Into Light" messy style
        const result = data.answer.toString();
        const text = new fabric.Text(result, {
          left: rightmost,
          top: topMost,
          fill: "#a6e3a1", // Mint green glow
          fontSize: 80,
          fontFamily: "'Shadows Into Light', cursive",
          selectable: true,
          angle: Math.random() * 6 - 3, // Slight tilt for handwritten look
        });

        canvas.add(text);
        canvas.setActiveObject(text);
        canvas.renderAll();
      } catch (err) {
        console.error("Sketch math error:", err);
        throw err;
      }
    },

    cleanDiagram() {
      const canvas = fabricRef.current;
      if (!canvas) return;
      const paths = canvas.getObjects().filter((o) => o.type === "path");
      paths.forEach((p) => processPath(p));
    },
  }));

  return (
    <div ref={containerRef} className="canvas-container">
      <canvas ref={canvasElRef} id="main-canvas" />
    </div>
  );
});

CanvasBoard.displayName = "CanvasBoard";
export default CanvasBoard;
