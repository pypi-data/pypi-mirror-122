class Footnote:
	def __init__(self, lead, others, citation):
		self.lead = lead.strip()
		self.others = others
		self.citation = citation.strip()
	
	def __str__(self):
		if self.others:
			return self.lead + ", " + self.others + ", " + self.citation
		else:
			return self.lead + ", " + self.citation