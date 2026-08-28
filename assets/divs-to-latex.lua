-- Map the book's fenced divs onto the LaTeX environments defined in
-- assets/preamble.tex, so one markdown source produces both the styled HTML
-- and a typeset PDF. Without this, pandoc emits the div's contents with no
-- environment at all and every box in the book silently loses its frame.
local ENVIRONMENTS = {
  definition = "qmibdefinition",
  archive    = "qmibarchive",
  warn       = "qmibwarn",
  step       = "qmibstep",
  check      = "qmibstep",
  lit        = "qmiblit",
  muted      = "qmibmuted",
  plate      = "qmibplate",
  plates     = "qmibplate",
}

function Div(el)
  if not FORMAT:match("latex") then return nil end
  for _, class in ipairs(el.classes) do
    local env = ENVIRONMENTS[class]
    if env then
      return {
        pandoc.RawBlock("latex", "\\begin{" .. env .. "}"),
        el,
        pandoc.RawBlock("latex", "\\end{" .. env .. "}"),
      }
    end
  end
  return nil
end

-- The archive and plate captions are spans, not divs.
function Span(el)
  if not FORMAT:match("latex") then return nil end
  for _, class in ipairs(el.classes) do
    if class == "archive-label" then
      return pandoc.Strong(el.content)
    elseif class == "plate-credit" or class == "term" then
      return el
    end
  end
  return nil
end
