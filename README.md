``` mermaid
graph LR
    INITIAL[statement]
    INITIAL -->statement_program[PROGRAMA]
    INITIAL -->def[def] --> id[ID]
    INITIAL -->left_par[L_PAR] --> parl["("]
    INITIAL -->r_part[R_PAR] --> parr[")"]
    INITIAL -->l_bracket[L_BRACKET] --> l_bracket_l["{"]
    INITIAL -->code[code]

    code --> expr[expr]
    INITIAL -->r_bracket[R_BRACKET] --> r_bracket_r["}"]
    expr --> s_init[statement init] & s_read[statement read] & ops[Operation] & printf[printf] & eend[end] & expr_r[EXPR]

    s_read --> read[READ] & ID[ID] & A[SEMICOLON]
    s_init --> INT[INT] & ids[ids] & B[SEMICOLON] 
    ops --> ID2[ID] & ASSIGN[ASSIGN] & ID3[ID] & PLUS[PLUS] & ID4[ID]
    printf --> PRINTF[PRINTF] & left_par2[L_PAR] & STRING[STRING] & R_PAR[RPAR]
    eend --> END[END] & SM[SEMICOLON]
    expr_r --> expr
```
