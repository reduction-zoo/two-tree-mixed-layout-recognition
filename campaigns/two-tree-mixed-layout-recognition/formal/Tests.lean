import Challenge
open TwoTreeMixedLayoutRecognition
example : isTwoTree ⟨3,[(0,1),(0,2),(1,2)]⟩ = true := by native_decide
example : isTwoTree ⟨3,[(0,1),(1,2)]⟩ = false := by native_decide
example : layout ⟨4,[(0,2),(1,3)]⟩ [0,1,2,3] [false,false] true = false := by native_decide
example : layout ⟨4,[(0,3),(1,2)]⟩ [0,1,2,3] [true,true] true = false := by native_decide
