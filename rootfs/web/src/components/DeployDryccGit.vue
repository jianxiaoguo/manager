<template>
    <li id="deploy-drycc-git" class="deploy-drycc-git list-group-item ember-view">
        <div class="panel-section ">
            <div class="section-description">
                <div class="section-title f3 bule" role="heading" aria-level="3">
                    Deploy using Drycc Git
                    <!---->    </div>

                <div class="mt2 f5 lh-copy dark-gray">
                    Use git in the command line or a Drycc cli tool to deploy this app.<br><a href="https://www.drycc.cc/applications/using-buildpacks/" class="hk-link">Learn more</a>
                </div>

                <!---->  </div>

            <div class="panel-content">
                <h4>Install the Drycc CLI</h4>
                <p>Download and install the <a href="https://www.drycc.cc/users/cli/" class="hk-link">Drycc CLI</a>.</p>

                <p>If you haven already, log in to your Drycc account.</p>

                <pre>$ drycc login {{cluster.url}}</pre>

                <h4>Add Drycc Git repository</h4>
                <p>For existing repositories, simply add the drycc remote.</p>
                <pre>$ drycc git:remote -a {{appDetail.name}}</pre>

                <h4>Generate an SSH Key</h4>
                <p>If you do not already have an SSH key or would like to create a new key for Drycc Workflow, generate a new key using.</p>
                <pre>$ ssh-keygen -f ~/.ssh/id_drycc -t rsa</pre>

                <h4>Add SSH Key</h4>
                <p>For application deploys via git push, Drycc Workflow identifies users via SSH keys. SSH keys are pushed to the platform and must be unique to each user.</p>
                <pre>$ drycc keys:add ~/.ssh/id_drycc.pub</pre>

                <h4>Push to Deploy</h4>
                <p>Commit your code to the repository and deploy it to Drycc using Git.</p>

                <pre>$ git push drycc main</pre>

                <div class="mt3 hk-message hk-message--info ember-view" role="alert"><!-- hk-messages are for hard coded copy only and uses {{{three brackets}}} so that we can include links in the title and or message -->

                        <div class="flex items-center">
                        
                        <div class="mr2">
                            <icon-branch-two class="icon malibu-icon" />
                        </div>
                        <div class="flex-auto flex flex-column tl">
                            <div class="flex-auto"></div>
                                <div class="lh-copy">
                                You can now change your main deploy branch from "master" to "main" for both manual and automatic deploys,
                                please follow the instructions <a href="https://git-scm.com/book/en/v2/Git-Branching-Branch-Management" class="hk-link nowrap">here</a>.
                                </div>
                            <div class="flex-auto"></div>
                        </div>
                        </div>
                </div>
            </div>
        </div>
    </li>
</template>

<script>
import DeployDryccGit from "./DeployDryccGit"
export default DeployDryccGit
</script>

<style scoped>

</style>
