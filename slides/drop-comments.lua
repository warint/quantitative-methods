-- HTML comments in a deck are notes for whoever edits the .qmd. Pandoc keeps
-- them as raw blocks, and Reveal turns any block that sits before the first
-- slide heading into a slide of its own: the empty slide 2 every deck had.
-- Dropping the comments removes it, and changes nothing a viewer could see.
function RawBlock(el)
  if el.format:match("html") and el.text:match("^%s*<!%-%-.*%-%->%s*$") then
    return {}
  end
end
