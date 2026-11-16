import collections

# For clarity, we round suss values to 3 decimal places

class SussVector(collections.UserDict) :
    "A dictionary-like class holding suss values for fields."
    def __add__(self,x) -> SussVector:
        """Add two SussVectors

        Logic: For each field, if just one vector has a corresponging value, use it.
        If both have fiel values and they are of different signs, return their sum
        Else return the average of field values
        """
        new = SussVector(self) # Prime with self data
        # If data only in self, we keep it as it is
        for k, val2 in x.items(): # iterate over values in x
            if k not in self:
                new[k] = x[k] # Value only in x
            elif self[k]*val2 < 0:
                new[k] = self[k] + val2
            else:
                new[k] = round((self[k] + val2)/2.0, 3)  # Average
        return new
