The National Geographical Institute takes aerial photographs in order to detect
changes on the earth's surface. In order to speed up this task they need a tool
that, given a photograph, is able to detect mountain borders. The images are
represented with matrices containing integers that represent the altitude of a
specific surface point. A set of connected points with the same altitude are
considered strata. The strata which are local minima are considered borders,
i.e. those strata whose points do not have lower altitude neighbors.
Design an algorithm that, given a matrix, returns a matrix having 0s in all
their elements but in the borders, where it has 1s.
(Source: hackealo.co)
