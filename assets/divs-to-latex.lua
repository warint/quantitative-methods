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


-- Wide tables get a page of their own, rotated.
--
-- The book prints dataframe previews — qmib.view() on the eleven-column course
-- spine, the fourteen-column questionnaire — and at a 6x9 trim those run off
-- the paper: one reached 871pt on a 432pt page. Rotating the page is the
-- conventional fix and keeps the table legible instead of shrinking it to
-- nothing. Narrow tables are untouched; only LaTeX is affected, since HTML
-- scrolls them sideways already.
local LANDSCAPE_MIN_COLUMNS = 7

function Table(el)
  if not FORMAT:match("latex") then return nil end

  local columns = 0
  if el.colspecs then
    columns = #el.colspecs
  end
  if columns < LANDSCAPE_MIN_COLUMNS then return nil end

  -- Rotating alone is not enough: eleven columns still overrun a rotated 6x9
  -- page. Shrink the type inside the environment, and drop the running head,
  -- which pdflscape otherwise rotates into the side of the table.
  return {
    pandoc.RawBlock("latex",
      "\\begin{landscape}\\thispagestyle{empty}\\begingroup\\scriptsize"),
    el,
    pandoc.RawBlock("latex", "\\endgroup\\end{landscape}"),
  }
end
