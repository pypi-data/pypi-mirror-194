from orwynn.base.error import Error


class FinalizedDiContainerError(Error):
    """If some evil force is trying to add objects to a finalized container.
    """
