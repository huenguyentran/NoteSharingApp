from django.views import View
from django.shortcuts import render, redirect
from core.views.BaseView import BaseView 

from notes.models import Note
from notes.forms.createNoteForm import CreateNoteForm
from workspaces.models import Workspace
from django.shortcuts import render, redirect, get_object_or_404 
from django.urls import reverse 

class createNoteView(BaseView):
    def get(self, request):
        form = CreateNoteForm()
        # No share_link is needed here as the note is not yet created.
        return render(request, 'create_note.html', {'form': form})

    def post(self, request):
        form = CreateNoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False) # Get the Note instance without saving yet
            note.create_by = request.user 

            # Handle workspace association
            workspace_id = request.GET.get('workspace_id')
            redirect_url = 'dashboard' # Default redirect

            if workspace_id:
                try:
                    # Retrieve workspace and ensure the user is a member
                    workspace = get_object_or_404(Workspace, pk=workspace_id, members__user=request.user)
                    note.workspace = workspace # Assign the note to this workspace
                    redirect_url = reverse('workspace_detail', kwargs={'pk': workspace.pk})
                except Exception as e:
                    print(f"Error assigning note to workspace (ID: {workspace_id}): {e}")
                    # You might want to add a message to the user here.
            
            # The 'is_shared_via_link' and 'link_permission' fields are handled by form.save()
            # because they are directly in the form's fields.
            # If is_shared_via_link is True, share_token will be automatically generated
            # by the model's default=uuid.uuid4.

            note.save() # Save the note to the database with all fields

            # After saving the note, if it's shared via link, we might want to
            # provide the link to the user. For creation, it's less common to
            # display it immediately, but for consistency, you could redirect
            # to the view_note page where the link can be shown.

            # Redirect to the detail page of the created note or the workspace
            if note.workspace:
                return redirect(reverse('workspace_detail', kwargs={'pk': note.workspace.pk}))
            else:
                # Assuming you have a URL named 'view_note' for individual notes
                return redirect(reverse('view_note', kwargs={'note_id': note.pk}))

        # If the form is not valid, re-render the form with errors
        return render(request, 'create_note.html', {'form': form})