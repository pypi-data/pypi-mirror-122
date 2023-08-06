all
rule 'MD024', :allow_different_nesting => true
rule 'MD013', :code_blocks => false, :line_length => false
exclude_rule 'MD012' # "Multiple consecutive blank lines"
exclude_rule 'MD001' # "Header levels should only increment by one level at a time"
