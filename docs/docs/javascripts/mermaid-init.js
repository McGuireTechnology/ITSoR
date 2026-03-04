document$.subscribe(() => {
  if (typeof mermaid === "undefined") {
    return;
  }

  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "loose",
    theme: document.body.getAttribute("data-md-color-scheme") === "slate" ? "dark" : "default",
  });

  const codeBlocks = document.querySelectorAll("pre.mermaid");
  codeBlocks.forEach((block) => {
    if (block.getAttribute("data-mermaid-processed") === "true") {
      return;
    }

    const codeNode = block.querySelector("code");
    const source = (codeNode ? codeNode.textContent : block.textContent) || "";

    const diagram = document.createElement("div");
    diagram.className = "mermaid";
    diagram.textContent = source.trim();

    block.setAttribute("data-mermaid-processed", "true");
    block.replaceWith(diagram);
  });

  mermaid.run({
    querySelector: "div.mermaid",
  });
});
